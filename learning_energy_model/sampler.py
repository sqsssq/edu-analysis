"""Gibbs sampling for pairwise binary energy models."""

from dataclasses import dataclass
from typing import Any

import torch


@dataclass
class SamplingResult:
    samples: torch.Tensor
    energies: torch.Tensor
    diagnostics: dict[str, Any]


class GibbsSampler:
    """Run independent Gibbs chains at temperature one."""

    def __init__(
        self,
        *,
        samples: int = 2_000,
        burn_in: int = 500,
        thinning: int = 1,
        chains: int = 4,
        seed: int = 0,
    ) -> None:
        if (
            not isinstance(samples, int)
            or not isinstance(burn_in, int)
            or not isinstance(thinning, int)
            or not isinstance(chains, int)
            or min(samples, chains) <= 0
            or burn_in < 0
            or thinning <= 0
        ):
            raise ValueError("samples and chains must be positive; burn_in must be non-negative")
        self.samples = samples
        self.burn_in = burn_in
        self.thinning = thinning
        self.chains = chains
        self.seed = seed

    def sample(
        self,
        h: torch.Tensor,
        J: torch.Tensor,
        *,
        clamp_index: int | None = None,
        clamp_value: float = 0.0,
        seed_offset: int = 0,
    ) -> SamplingResult:
        """Return post-burn-in samples and simple convergence diagnostics."""
        self._validate_parameters(h, J)
        if clamp_index is not None and not 0 <= clamp_index < h.numel():
            raise ValueError("clamp_index is outside the model node range")
        if clamp_value not in {0.0, 1.0}:
            raise ValueError("clamp_value must be 0 or 1")
        generator = torch.Generator(device=h.device)
        generator.manual_seed(self.seed + seed_offset)
        total_steps = self.burn_in + self.samples * self.thinning
        chain_samples = []
        chain_energies = []
        for _ in range(self.chains):
            state = torch.randint(
                0, 2, (h.numel(),), device=h.device, generator=generator, dtype=torch.int64
            ).to(torch.float64)
            if clamp_index is not None:
                state[clamp_index] = clamp_value
            collected = []
            for step in range(total_steps):
                for index in torch.randperm(h.numel(), device=h.device, generator=generator):
                    node = int(index)
                    if node == clamp_index:
                        continue
                    local_field = h[node] + torch.dot(J[node], state)
                    probability = torch.sigmoid(-local_field)
                    state[node] = (
                        torch.rand((), device=h.device, generator=generator) < probability
                    ).to(torch.float64)
                if clamp_index is not None:
                    state[clamp_index] = clamp_value
                if step >= self.burn_in and (step - self.burn_in) % self.thinning == 0:
                    collected.append(state.clone())
            samples = torch.stack(collected)
            chain_samples.append(samples)
            chain_energies.append(samples @ h + 0.5 * ((samples @ J) * samples).sum(dim=1))

        by_chain = torch.stack(chain_samples)
        energies = torch.stack(chain_energies)
        flat_samples = by_chain.reshape(-1, h.numel())
        chain_means = by_chain.mean(dim=1)
        within = by_chain.var(dim=1, unbiased=True).mean(dim=0)
        between = chain_means.var(dim=0, unbiased=True)
        variance = ((self.samples - 1) / self.samples) * within + between / self.samples
        stable = within > 1e-12
        rhat = torch.where(
            stable,
            torch.sqrt(torch.clamp(variance / within, min=0.0)),
            torch.where(between <= 1e-12, torch.ones_like(within), torch.full_like(within, float("inf"))),
        )
        effective_size = self._effective_sample_size(by_chain, within)
        return SamplingResult(
            samples=flat_samples,
            energies=energies.reshape(-1),
            diagnostics={
                "chains": float(self.chains),
                "draws": float(flat_samples.shape[0]),
                "max_rhat": float(rhat.max()),
                "min_effective_sample_size": float(effective_size.min()),
                "rhat_by_node": rhat.detach().cpu().tolist(),
                "effective_sample_size_by_node": effective_size.detach().cpu().tolist(),
            },
        )

    @staticmethod
    def _validate_parameters(h: torch.Tensor, J: torch.Tensor) -> None:
        if h.ndim != 1 or J.ndim != 2 or J.shape != (h.numel(), h.numel()):
            raise ValueError("h must be one-dimensional and J must be a matching square matrix")
        if not torch.is_floating_point(h) or not torch.is_floating_point(J):
            raise ValueError("h and J must use floating-point tensors")
        if not torch.isfinite(h).all() or not torch.isfinite(J).all():
            raise ValueError("h and J must contain only finite values")
        if not torch.allclose(J, J.T):
            raise ValueError("J must be symmetric")

    def _effective_sample_size(
        self, by_chain: torch.Tensor, within: torch.Tensor
    ) -> torch.Tensor:
        """Estimate ESS from the initial positive autocorrelation sequence."""
        n_draws = by_chain.shape[1]
        total = float(by_chain.shape[0] * n_draws)
        if n_draws < 2:
            return torch.ones(by_chain.shape[2], dtype=torch.float64, device=by_chain.device)
        centered = by_chain - by_chain.mean(dim=1, keepdim=True)
        autocorrelation_sum = torch.zeros_like(within)
        active = torch.ones_like(within, dtype=torch.bool)
        for lag in range(1, min(100, n_draws - 1) + 1):
            autocovariance = (
                centered[:, :-lag, :] * centered[:, lag:, :]
            ).mean(dim=1).mean(dim=0)
            correlation = autocovariance / torch.clamp(within, min=1e-12)
            active &= correlation > 0
            autocorrelation_sum += torch.where(active, correlation, torch.zeros_like(correlation))
        return torch.clamp(
            total / torch.clamp(1.0 + 2.0 * autocorrelation_sum, min=1.0),
            min=1.0,
            max=total,
        )

    def moments(
        self,
        h: torch.Tensor,
        J: torch.Tensor,
        *,
        clamp_index: int | None = None,
        clamp_value: float = 0.0,
        seed_offset: int = 0,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, dict[str, Any]]:
        result = self.sample(
            h,
            J,
            clamp_index=clamp_index,
            clamp_value=clamp_value,
            seed_offset=seed_offset,
        )
        means = result.samples.mean(dim=0)
        pairwise = result.samples.T @ result.samples / result.samples.shape[0]
        return means, pairwise, result.energies, result.diagnostics
