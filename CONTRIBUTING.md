# Contributing to BlueSentra

Rules come from ADR-019 (Git workflow) and ADR-018 (code quality).

- Trunk-based development: `main` is always deployable, and direct commits to it are prohibited.
- Short-lived branches named `feature/...`, `fix/...` or `chore/...`, merged as small vertical slices.
- Conventional Commits: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`, `perf`, `build`, `ci`.
  Example: `feat(auth): add role-scoped JWT authentication`.
- CI must pass before merging. Review is preferred.
- Squash merge without review is a documented exception, not the default. Authentication and
  RBAC changes get a second-person review whenever feasible.
- Delete branches after merging.
- A passing frontend test never substitutes for a passing backend authorization test.
