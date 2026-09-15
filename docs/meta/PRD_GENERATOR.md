# PRD Generator Guide

Use this guide when a product idea is too vague to implement safely.

## Goal

Turn a rough project idea into PRD updates that an AI coding agent can use for small implementation tasks.

## Required Framing

Every PRD update should clarify:

- primary user,
- MVP loop,
- domain-specific quality rules,
- explicit non-goals,
- verification strategy,
- open questions.

## PRD Output Rules

- Keep MVP scope narrow unless the user explicitly changes the PRD.
- Do not add backend, database, authentication, deployment, or AI API scope by default.
- Do not turn the project into its generic failure mode.
- Record decisions in `docs/prd/09-decision-log.md`.
- Record unresolved issues in `docs/prd/08-open-questions.md`.
- Update `docs/domain/PROJECT_RULES.md` when a domain-specific rule is discovered.
