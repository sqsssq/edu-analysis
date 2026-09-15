"""Gibbs sampling for pairwise binary energy models."""

from dataclasses import dataclass

import torch


@dataclass
class SamplingResult:
    samples: torch.Tensor
    energies: torch.Tensor
    diagnostics: dict[str, float]


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
        if min(samples, chains) <= 0 or burn_in < 0 or thinning <= 0:
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
        within = by_chain.var(dim=1, unbiased=False).mean(dim=0)
        between = chain_means.var(dim=0, unbiased=False)
        variance = ((self.samples - 1) / self.samples) * within + between
        rhat = torch.sqrt(torch.clamp(variance / torch.clamp(within, min=1e-12), min=0.0))
        effective_size = torch.full_like(rhat, float(flat_samples.shape[0]))
        return SamplingResult(
            samples=flat_samples,
            energies=energies.reshape(-1),
            diagnostics={
                "chains": float(self.chains),
                "draws": float(flat_samples.shape[0]),
                "max_rhat": float(rhat.max()),
                "min_effective_sample_size": float(effective_size.min()),
            },
        )

    def moments(
        self,
        h: torch.Tensor,
        J: torch.Tensor,
        *,
        clamp_index: int | None = None,
        clamp_value: float = 0.0,
        seed_offset: int = 0,
    ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, dict[str, float]]:
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
