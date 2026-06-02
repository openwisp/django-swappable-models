# AGENTS.md

## Project Overview

`django-swappable-models` provides the `swapper` utility used by OpenWISP Django apps to support swappable models.

Core code lives in `swapper/`:

- `__init__.py` contains the public model loading and dependency helpers.
- Tests live in `tests/`, including default and alternate apps for swapped-model behavior.

## Source of Truth

- Use `README.md` for setup, package usage, and baseline test commands.
- Use `.github/workflows/ci.yml` and `tox.ini` for CI-tested dependencies, QA/test commands, env vars, and supported Python/Django versions.
- Use GitHub issue/PR templates when asked to open issues or PRs.

If instructions conflict, repository config and CI workflows win first, docs next, and this file is supplemental.

## Development Notes

- Keep changes focused. Avoid unrelated refactors and formatting churn.
- Preserve public APIs, import-time behavior, Django app registry behavior, migration dependency helpers, and backward compatibility unless explicitly required.
- Avoid unnecessary blank lines inside function and method bodies.
- Update docs when behavior, settings, public APIs, setup steps, or supported versions change.

## Testing and QA

- Add or update tests for every behavior change.
- For bug fixes, write the regression test first, run it against the unfixed code, confirm it fails for the expected reason, then implement the fix.
- Use targeted tests while iterating, then run the documented full test command before considering the change complete.
- Run `openwisp-qa-format` after editing when available.
- Run `./run-qa-checks` when present. Treat failures as blocking unless confirmed unrelated and reported.
- Prefer in-process tests so coverage tools can measure changed code.

## Django Notes

- Cover both default and swapped-model apps when changing model resolution, dependency generation, or settings handling.
- Be careful with import timing, circular imports, app labels, migration dependencies, and Django version compatibility.

## Security Notes

- Watch for unsafe dynamic imports, incorrect model resolution, and secrets in tests or docs.
- Write comments and docstrings only when they explain why code is shaped a certain way. Put comments before the relevant code block instead of scattering them inside it.

## Troubleshooting

- If setup, QA, or tests fail, check docs first, then compare with CI. If commands diverge, follow CI.
