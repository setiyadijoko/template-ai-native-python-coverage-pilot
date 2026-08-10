# Hosted Python Coverage Consumer Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and validate a minimal public Python consumer that proves the template's hosted quality, duplicate-name-safe aggregate coverage, build, security, and post-merge provenance path.

**Architecture:** A dependency-free `coverage_pilot` library exposes one deterministic priority classifier. Unit, integration, and end-to-end suites intentionally reuse `test_priority.py`; the consumer supplies no pytest discovery workaround, so the inherited template command owns fixture exclusion and import collision safety.

**Tech Stack:** Python 3.12+, setuptools 80.9.0, Ruff 0.15.22, mypy 2.3.0, pytest 9.1.1, pytest-cov 7.1.0, build 1.5.0, POSIX shell, Make, GitHub Actions.

## Global Constraints

- Repository remains public at `setiyadijoko/template-ai-native-python-coverage-pilot`.
- Layout is `single`; primary stack is `python`; package code lives under `src/coverage_pilot/`.
- Maturity profile is declarative `standard`; profile settings do not activate or alter workflows.
- AI and deployment are disabled; no secret, provider endpoint, database, API framework, or deployment target is introduced.
- Do not add pytest `testpaths`, `pythonpath`, `addopts`, `--ignore`, or `import-mode` configuration in `pyproject.toml`.
- Do not modify inherited files under `.github/workflows/`.
- Overall coverage must remain at least 80%; do not lower the threshold or add assertion-free tests.
- GitHub-hosted results are authoritative for hosted-runner and attestation claims.

---

### Task 1: Initialize the consumer and deterministic Python toolchain

**Files:**
- Modify: `README.md`
- Create: `.template/project.yaml`
- Create: `.template/profile.yaml`
- Create: `pyproject.toml`

**Interfaces:**
- Consumes: inherited `scripts/init-project.sh`, profile schema, stack detector, and Python dependency bootstrap.
- Produces: validated single-stack consumer metadata and a reproducible Python build/development contract used by every later task.

- [ ] **Step 1: Initialize README identity and project layout**

Run:

```sh
sh scripts/init-project.sh \
  --name "Python Coverage Pilot" \
  --description "Disposable hosted Python consumer for template-ai-native coverage and CI validation." \
  --stack python \
  --layout single
```

Expected: exit `0`, README identity is replaced once, and
`.template/project.yaml` contains version `1`, layout `single`, primary stack
`python`, and primary path `src`.

- [ ] **Step 2: Add the approved Standard profile**

Create `.template/profile.yaml` with exactly:

```yaml
version: 1
profile: standard
project:
  type: library
stack:
  primary: python
ai:
  enabled: false
  evaluation: false
  semantic_review: off
  structural_review: off
deployment:
  enabled: false
  target: none
controls:
  secret_scan: true
  dependency_review: true
  codeql: true
  coverage: true
  sbom: false
  artifact_attestation: true
  scorecard: false
```

- [ ] **Step 3: Add the pinned Python package contract**

Create `pyproject.toml` with exactly:

```toml
[build-system]
requires = ["setuptools==80.9.0"]
build-backend = "setuptools.build_meta"

[project]
name = "template-ai-native-python-coverage-pilot"
version = "0.1.0"
description = "Disposable hosted Python coverage consumer pilot"
requires-python = ">=3.12"

[project.optional-dependencies]
dev = [
  "ruff==0.15.22",
  "mypy==2.3.0",
  "pytest==9.1.1",
  "pytest-cov==7.1.0",
  "build==1.5.0",
]

[tool.setuptools.packages.find]
where = ["src"]

[tool.mypy]
strict = true

[tool.ruff]
line-length = 88
```

The file intentionally contains no pytest configuration section.

- [ ] **Step 4: Bootstrap dependencies in an isolated environment**

Run:

```sh
python3 -m venv .venv
PYTHON_BIN=.venv/bin/python sh scripts/setup-python-deps.sh
```

Expected: exit `0`; the editable consumer and every pinned development tool
are installed under `.venv`.

- [ ] **Step 5: Validate metadata and stack resolution**

Run:

```sh
sh scripts/validate-project-config.sh
sh scripts/validate-profile-config.sh
test "$(sh scripts/detect-stack.sh)" = python
```

Expected: both validators exit `0` and stack detection returns `python`.

- [ ] **Step 6: Review and commit configuration**

Run:

```sh
git diff --check
git diff -- README.md .template/project.yaml .template/profile.yaml pyproject.toml
git add README.md .template/project.yaml .template/profile.yaml pyproject.toml
git commit -m "chore: initialize Python coverage pilot"
```

Expected: one configuration-only commit with no workflow or application code
change.

---

### Task 2: Implement the classifier through one complete TDD cycle

**Files:**
- Create: `tests/unit/test_priority.py`
- Create: `tests/integration/test_priority.py`
- Create: `tests/e2e/test_priority.py`
- Create: `src/coverage_pilot/__init__.py`
- Create: `src/coverage_pilot/priority.py`

**Interfaces:**
- Consumes: Python package/tool contract from Task 1.
- Produces: `Priority` and `classify_priority(*, severity: int, customer_impact: bool) -> Priority` through the public `coverage_pilot` package.

- [ ] **Step 1: Write the unit contract before implementation**

Create `tests/unit/test_priority.py`:

```python
import pytest

from coverage_pilot import Priority, classify_priority


@pytest.mark.parametrize(
    ("severity", "customer_impact", "expected"),
    [
        (1, False, Priority.P1),
        (1, True, Priority.P1),
        (2, False, Priority.P2),
        (2, True, Priority.P1),
        (3, False, Priority.P3),
        (3, True, Priority.P2),
        (4, False, Priority.P4),
        (4, True, Priority.P3),
    ],
)
def test_classifies_literal_priority_matrix(
    severity: int,
    customer_impact: bool,
    expected: Priority,
) -> None:
    assert (
        classify_priority(
            severity=severity,
            customer_impact=customer_impact,
        )
        is expected
    )


@pytest.mark.parametrize("severity", [0, 5])
def test_rejects_severity_outside_supported_range(severity: int) -> None:
    with pytest.raises(ValueError, match="severity must be between 1 and 4"):
        classify_priority(severity=severity, customer_impact=False)
```

- [ ] **Step 2: Write integration and E2E contracts with the same basename**

Create `tests/integration/test_priority.py`:

```python
from coverage_pilot import Priority, classify_priority


def test_public_package_boundary_classifies_customer_impact() -> None:
    result = classify_priority(severity=3, customer_impact=True)

    assert result is Priority.P2
```

Create `tests/e2e/test_priority.py`:

```python
from coverage_pilot import Priority, classify_priority


def test_operational_signal_sequence_produces_expected_priorities() -> None:
    signals = [(4, False), (3, True), (2, True), (1, False)]

    actual = [
        classify_priority(severity=severity, customer_impact=customer_impact)
        for severity, customer_impact in signals
    ]

    assert actual == [Priority.P4, Priority.P2, Priority.P1, Priority.P1]
```

- [ ] **Step 3: Verify all three tests fail for the intended reason**

Run:

```sh
PATH="$PWD/.venv/bin:$PATH" pytest -q tests/unit
PATH="$PWD/.venv/bin:$PATH" pytest -q tests/integration
PATH="$PWD/.venv/bin:$PATH" pytest -q tests/e2e
```

Expected: every command fails during collection with
`ModuleNotFoundError: No module named 'coverage_pilot'`. Fix import typos before
continuing if the failure differs.

- [ ] **Step 4: Implement the minimum package**

Create `src/coverage_pilot/priority.py`:

```python
from enum import StrEnum


class Priority(StrEnum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


def classify_priority(*, severity: int, customer_impact: bool) -> Priority:
    if severity not in range(1, 5):
        raise ValueError("severity must be between 1 and 4")

    level = severity - int(customer_impact)
    return Priority(f"P{max(1, level)}")
```

Create `src/coverage_pilot/__init__.py`:

```python
from coverage_pilot.priority import Priority, classify_priority

__all__ = ["Priority", "classify_priority"]
```

- [ ] **Step 5: Verify categorized tests and aggregate coverage**

Run:

```sh
PATH="$PWD/.venv/bin:$PATH" make test-unit
PATH="$PWD/.venv/bin:$PATH" make test-integration
PATH="$PWD/.venv/bin:$PATH" make test-e2e
PATH="$PWD/.venv/bin:$PATH" make test-coverage
```

Expected: every category passes; aggregate coverage collects all three
same-named files, does not collect `tests/fixtures/`, and reports at least 80%.

- [ ] **Step 6: Verify format, lint, and types**

Run:

```sh
PATH="$PWD/.venv/bin:$PATH" make format-check
PATH="$PWD/.venv/bin:$PATH" make lint
PATH="$PWD/.venv/bin:$PATH" make typecheck
```

Expected: all commands exit `0` with no formatting, Ruff, or mypy errors.

- [ ] **Step 7: Review and commit the TDD slice**

Run:

```sh
git diff --check
git diff -- src/coverage_pilot tests/unit/test_priority.py tests/integration/test_priority.py tests/e2e/test_priority.py
git add src/coverage_pilot tests/unit/test_priority.py tests/integration/test_priority.py tests/e2e/test_priority.py
git commit -m "feat: add deterministic priority classifier"
```

Expected: one application commit containing the three tests and their minimum
implementation.

---

### Task 3: Complete local consumer verification and documentation

**Files:**
- Modify: `CHANGELOG.md`
- Modify: `docs/superpowers/specs/2026-08-10-python-coverage-consumer-pilot-design.md`

**Interfaces:**
- Consumes: configured consumer and classifier from Tasks 1-2.
- Produces: locally verified build artifacts and truthful documentation state ready for hosted review.

- [ ] **Step 1: Record the implemented local pilot state**

Under `CHANGELOG.md` → `## [Unreleased]` → `### Added`, add:

```markdown
- Added a deterministic Python coverage pilot with same-named unit,
  integration, and E2E test modules to validate template-owned fixture
  isolation and aggregate coverage behavior.
```

Change the design status to:

```markdown
**Status:** Implemented locally; hosted validation pending
```

- [ ] **Step 2: Run all application-level gates**

Run:

```sh
PATH="$PWD/.venv/bin:$PATH" make format-check
PATH="$PWD/.venv/bin:$PATH" make lint
PATH="$PWD/.venv/bin:$PATH" make typecheck
PATH="$PWD/.venv/bin:$PATH" make test-unit
PATH="$PWD/.venv/bin:$PATH" make test-integration
PATH="$PWD/.venv/bin:$PATH" make test-e2e
PATH="$PWD/.venv/bin:$PATH" make test-coverage
PATH="$PWD/.venv/bin:$PATH" make build
```

Expected: every command exits `0`; `dist/` contains one wheel and one source
distribution.

- [ ] **Step 3: Run template, documentation, and security gates**

Run:

```sh
PATH="$PWD/.venv/bin:$PATH" make test-scripts
PATH="$PWD/.venv/bin:$PATH" make docs-check
PATH="$PWD/.venv/bin:$PATH" make security
PATH="$PWD/.venv/bin:$PATH" make ci
```

Expected: every command exits `0`. Record optional documentation tools that
skip because they are unavailable; do not report them as executed.

- [ ] **Step 4: Inspect generated artifacts and complete diff**

Run:

```sh
find dist -maxdepth 1 -type f -print | sort
git status --short
git diff --check
git diff
```

Expected: build outputs exist but remain ignored; only the intended changelog
and design-status edits are uncommitted; no cache, environment, secret, or
generated build file is staged.

- [ ] **Step 5: Commit documentation state**

Run:

```sh
git add CHANGELOG.md docs/superpowers/specs/2026-08-10-python-coverage-consumer-pilot-design.md
git commit -m "docs: record local Python pilot evidence"
```

Expected: one documentation-only commit.

---

### Task 4: Open and verify the hosted consumer pull request

**Files:**
- No repository file changes expected.

**Interfaces:**
- Consumes: the locally verified implementation branch.
- Produces: a Draft PR and GitHub-hosted evidence for Python quality, categorized tests, coverage, build, and blocking security controls.

- [ ] **Step 1: Verify branch scope before publication**

Run:

```sh
git status -sb
git log --oneline origin/main..HEAD
git diff --check origin/main...HEAD
git diff --stat origin/main...HEAD
```

Expected: clean worktree and only the approved design, plan, configuration,
classifier, tests, changelog, and consumer identity changes.

- [ ] **Step 2: Push the implementation branch**

Run:

```sh
git push -u origin agent/python-coverage-pilot-design
```

Expected: the remote branch advances to the local HEAD without force push.

- [ ] **Step 3: Open the Draft PR**

Create a Draft PR to `main` with title:

```text
test: validate hosted Python coverage consumer
```

The body must state the pilot purpose, intentional repeated test basenames,
absence of consumer pytest workarounds, local commands actually executed, and
known best-effort tool skips.

- [ ] **Step 4: Inspect every hosted check**

Run:

```sh
gh pr checks --watch --interval 10
gh pr view --json number,url,state,isDraft,headRefOid,statusCheckRollup
```

Expected: stack detection returns Python; Python quality, integration/E2E/
coverage, build, CodeQL, dependency review, secret scan, documentation, and
workflow-security checks succeed. AI/deployment-related skips remain expected.

- [ ] **Step 5: Report hosted findings without merging**

Record the PR URL, head commit, check names, conclusions, workflow run links,
coverage result, build artifact name, expected skips, and any discrepancy.
The repository owner decides whether to merge.

---

### Task 5: Verify post-merge artifact provenance

**Files:**
- No repository file changes expected unless a separate evidence document is explicitly approved.

**Interfaces:**
- Consumes: owner-approved merge to `main` and the resulting `ci.yml` run.
- Produces: verified artifact digest and GitHub attestation evidence used for the shadow-mode go/no-go decision.

- [ ] **Step 1: Locate the push-to-main CI run**

Run:

```sh
gh run list \
  --repo setiyadijoko/template-ai-native-python-coverage-pilot \
  --branch main \
  --workflow ci.yml \
  --limit 1 \
  --json databaseId,status,conclusion,headSha,url
```

Expected: the newest run targets the merge commit and concludes `success`.

- [ ] **Step 2: Verify jobs and download the build artifact**

Resolve the newest successful run and use its database ID directly:

```sh
pilot_run_id="$(gh run list \
  --repo setiyadijoko/template-ai-native-python-coverage-pilot \
  --branch main \
  --workflow ci.yml \
  --limit 1 \
  --json databaseId \
  --jq '.[0].databaseId')"
test -n "$pilot_run_id"
gh run view "$pilot_run_id" \
  --repo setiyadijoko/template-ai-native-python-coverage-pilot \
  --json headSha,status,conclusion,jobs,url
gh run download "$pilot_run_id" \
  --repo setiyadijoko/template-ai-native-python-coverage-pilot \
  --name build-python \
  --dir /private/tmp/template-ai-native-python-coverage-pilot-artifact
```

Expected: Python build and attestation jobs succeed; exactly one packaged file
named `template-ai-native-build-python.tar.gz` is downloaded.

- [ ] **Step 3: Compute and verify the attested digest**

Run:

```sh
shasum -a 256 /private/tmp/template-ai-native-python-coverage-pilot-artifact/template-ai-native-build-python.tar.gz
gh attestation verify \
  /private/tmp/template-ai-native-python-coverage-pilot-artifact/template-ai-native-build-python.tar.gz \
  --repo setiyadijoko/template-ai-native-python-coverage-pilot
```

Expected: the local SHA-256 is reported and GitHub verifies a signed build
provenance attestation for this repository and artifact.

- [ ] **Step 4: Issue the shadow-mode readiness decision**

Report exact local and hosted evidence, attestation verification, expected
skips, remaining risks, and one decision:

- `GO` only if every acceptance criterion in the approved design is evidenced.
- `NO-GO` if a Python job skipped, coverage used a consumer workaround, build
  or security failed, or provenance could not be verified.

Do not enable profile-aware shadow-mode workflows as part of this pilot.
