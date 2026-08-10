# Hosted Python Coverage Consumer Pilot Design

**Status:** Implemented locally; hosted validation pending
**Date:** 2026-08-10
**Repository:** `setiyadijoko/template-ai-native-python-coverage-pilot`

## Purpose

Prove that a new public consumer generated from `template-ai-native` can run
the Python quality, categorized-test, aggregate-coverage, build, security, and
post-merge provenance path on GitHub-hosted runners without consumer-specific
workarounds for template fixture discovery or duplicate test module names.

This repository is disposable validation evidence. It is not a production
application or a reusable Python starter.

## Decision

Build a minimal deterministic Python library named `coverage_pilot`. The
library classifies an operational signal into `P1`, `P2`, `P3`, or `P4` from
two explicit inputs: severity and customer impact. It has no runtime
dependencies, network calls, persistence, API, AI model, or deployment target.

Use the same test filename in unit, integration, and end-to-end directories.
Do not add consumer-owned pytest `testpaths`, `--ignore`, or `import-mode`
configuration. This makes the template's aggregate coverage command solely
responsible for excluding `tests/fixtures/` and avoiding module collisions.

## Alternatives considered

### CLI application

A CLI would test argument parsing and executable packaging, but those concerns
do not contribute evidence for the coverage-discovery contract and would add
unnecessary implementation surface.

### FastAPI service

An API would exercise runtime dependency installation, but installing FastAPI
would hide the fixture-isolation regression that this pilot is intended to
detect. Hosted Python dependency bootstrap has already been validated in an
earlier consumer pilot.

## Repository configuration

- Visibility: public.
- Source: the current `main` branch of `setiyadijoko/template-ai-native`.
- Layout: `single`.
- Primary stack: `python`.
- Maturity profile: `standard`.
- AI capability: disabled.
- Deployment: disabled with target `none`.
- No repository, environment, or Actions secrets are required.
- Production readiness remains false because the repository has no deployment
  target and is intentionally disposable.

The profile is declarative evidence only. It must not activate or alter
workflow behavior during this pilot.

## Components

### Package contract

`src/coverage_pilot/priority.py` exposes:

```python
from enum import StrEnum


class Priority(StrEnum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


def classify_priority(*, severity: int, customer_impact: bool) -> Priority:
    ...
```

The function accepts severity values from 1 through 4. Values outside that
range raise `ValueError`. Customer impact raises the priority by one level,
capped at `P1`. The deterministic mapping is:

| Severity | No customer impact | Customer impact |
|---:|:---:|:---:|
| 1 | P1 | P1 |
| 2 | P2 | P1 |
| 3 | P3 | P2 |
| 4 | P4 | P3 |

### Test boundaries

- `tests/unit/test_priority.py` verifies the complete literal mapping and
  invalid severity values.
- `tests/integration/test_priority.py` verifies the public package import and
  a representative classification through that boundary.
- `tests/e2e/test_priority.py` verifies a small sequence of operational inputs
  produces the expected priority sequence.

The repeated basename `test_priority.py` is intentional. Category-specific
commands and aggregate coverage must both succeed.

### Build contract

`pyproject.toml` uses a `src/` package layout and a pinned setuptools/wheel
build backend. Development dependencies pin Ruff, mypy, pytest, pytest-cov,
and build so hosted behavior is reproducible. The build must produce both a
wheel and source distribution under `dist/`.

## Execution flow

1. Initialize the consumer identity and single-stack project configuration.
2. Add the Standard declarative profile.
3. Write tests before implementation and observe the expected import failure.
4. Implement the smallest deterministic package that satisfies the tests.
5. Run local quality, categorized tests, aggregate coverage, build, security,
   documentation, and repository-native CI checks.
6. Push the implementation branch and open a pull request to `main`.
7. Record hosted PR check results without changing required-check policy.
8. Merge only after the owner reviews the evidence.
9. Verify the push-to-main build and provenance attestation use the resulting
   build artifact.

## Failure handling

- A collected template fixture is a pilot failure; do not install FastAPI to
  hide it.
- A duplicate-module import error is a pilot failure; do not add consumer
  pytest discovery or import-mode configuration to hide it.
- Coverage below 80% is a pilot failure; add meaningful behavioral tests and
  do not lower the threshold.
- A missing or invalid build artifact is a pilot failure.
- A skipped hosted Python job after stack detection is a pilot failure.
- Expected skips for disabled AI, deployment, and template-only controls are
  recorded but do not fail this pilot.
- GitHub-hosted results are authoritative for hosted-runner claims; local
  success alone does not complete the pilot.

## Security and governance

- No credentials, tokens, personal data, or external service endpoints enter
  the repository.
- Existing least-privilege workflow permissions and immutable Action pins are
  inherited unchanged from the template.
- The pilot uses `pull_request`, never `pull_request_target`.
- AI review remains advisory and secret-gated.
- No production environment or deployment authority is configured.
- The complete diff is reviewed before every commit and no template workflow
  is modified in the consumer.

## Acceptance criteria

- The public repository exists under `setiyadijoko` with a generated initial
  commit derived from the template's current `main` content.
- Stack detection returns `python`.
- Project and Standard profile configuration validate.
- Format check, Ruff, mypy, unit, integration, and E2E commands pass.
- Aggregate coverage collects all three test categories, does not collect
  `tests/fixtures/`, tolerates identical test basenames, and reports at least
  80% coverage.
- `make build` creates a wheel and source distribution.
- `make test-scripts`, `make docs-check`, and `make ci` complete successfully,
  with optional locally unavailable documentation tools reported accurately.
- Hosted pull-request Python quality, integration/E2E/coverage, build, and
  blocking security checks succeed.
- After merge, GitHub creates signed build provenance for the produced Python
  artifact.
- No consumer-specific pytest discovery workaround, secret, deployment, AI
  provider, API framework, database, or unrelated feature is introduced.

## Out of scope

- Profile-aware workflow activation or shadow-mode implementation.
- Branch-protection changes.
- API authentication, persistence, observability backend, and deployment.
- Performance, DAST, canary, disaster recovery, or real-model evaluation.
- General-purpose Python project scaffolding.

## Completion evidence

The final pilot report must identify the repository and pull request, exact
commits, local commands and results, hosted workflow run identifiers, artifact
names and digests, attestation URL, expected skips, findings, and whether the
evidence supports proceeding to profile-aware shadow-mode design.
