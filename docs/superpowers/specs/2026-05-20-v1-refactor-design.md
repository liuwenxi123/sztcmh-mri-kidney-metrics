# 2026-05-20 V1 Refactor Design

## Goal

Modernize the original `Pixel-Counter2` codebase into a maintainable desktop application while preserving the current research workflows and core output behavior. This v1 pass focuses on architecture, naming, module boundaries, reproducibility, and testability rather than redesigning the product experience.

## Project Identity

- Working repository name: `sztcmh-mri-kidney-metrics`
- Current baseline tag: `v0-code-0`
- V1 target: a behavior-preserving refactor with a clean package layout, service layer, tests, and minimal user-facing disruption.

## Current Problems

1. The project root mixes source code, build outputs, caches, archives, sample data, and generated spreadsheets.
2. UI widgets directly own domain logic, filesystem traversal, image loading, calculations, and Excel export.
3. Multiple workflows reuse copied logic instead of shared, testable services.
4. Naming is inconsistent and partially legacy-oriented, which obscures intent.
5. The `vMRE-sADC` functionality exists as both an unfinished widget and a separate script, so the behavior boundary is unclear.
6. There is no stable automated verification path for the calculation logic.

## Recommended Approach

Use a behavior-preserving layered refactor.

### Why this approach

- It creates clear seams without forcing a full product rewrite.
- It preserves the historical baseline established in `v0-code-0`.
- It lets us move the high-risk math and file operations under tests before larger UX changes.
- It keeps room for a stronger v2 redesign later.

## Alternatives Considered

### Option A: Minimal tidy-up

Move a few files, add a README, and keep most logic in widgets.

- Pros: fastest, lowest short-term risk.
- Cons: weak long-term payoff, difficult to test, poor base for v2.

### Option B: Behavior-preserving layered refactor (recommended)

Create a small application package with dedicated modules for workflows and calculations, while keeping the existing functional scope.

- Pros: good maintainability, bounded risk, testable core.
- Cons: moderate implementation effort.

### Option C: Full rewrite now

Rebuild the application with a new UI and redesigned workflows immediately.

- Pros: maximum cleanup.
- Cons: highest regression risk, weak continuity with historical behavior.

## Target Architecture

The v1 architecture will be organized around a Python package under `src/sztcmh_mri_kidney_metrics`.

### Layers

1. `app`
   - Application bootstrap, window composition, app metadata.
2. `ui`
   - PyQt widgets and view helpers only.
   - No direct calculation logic or raw filesystem traversal beyond delegating to services.
3. `services`
   - File extraction, rename, conversion, export, and orchestration helpers.
4. `domain`
   - Pure calculation logic for kidney metrics and vMRE/sADC processing.
5. `models`
   - Dataclasses for metric outputs, requests, and configuration payloads.
6. `tests`
   - Unit tests for pure domain logic and service-level behavior.

## Proposed Directory Layout

```text
sztcmh-mri-kidney-metrics/
  README.md
  pyproject.toml
  .gitignore
  docs/
    superpowers/
      specs/
      plans/
  src/
    sztcmh_mri_kidney_metrics/
      __init__.py
      app/
      ui/
      services/
      domain/
      models/
      resources/
  tests/
    unit/
    fixtures/
  data/
    samples/
  scripts/
```

## Functional Mapping

### 1. File Extraction

Current source: `FileFetch_Widget.py`

V1 split:
- UI form for folder selection and mode selection.
- Service for recursive extraction based on search rules.
- Model for extraction request.

### 2. Pixel Metrics

Current source: `PixelCalculater_Widget.py`, `cal.py`, `cal_use.py`

V1 split:
- Domain functions for full-volume and middle-slice metrics.
- Service for loading NIfTI pairs and coordinating exports.
- Result models for all-kidney, left-kidney, and right-kidney metrics.
- UI only displays and triggers these workflows.

### 3. Batch Rename

Current source: `Rename_Widget.py`

V1 split:
- Service for rename preview and execution.
- UI for input and result messages.

### 4. NIfTI Conversion

Current source: `ConvNII_Widget.py`

V1 split:
- Service for `.nii` <-> `.nii.gz` conversion.
- UI for path selection and confirmation.

### 5. vMRE-sADC Workflow

Current source: `vMRE-sADC.py`, `vMREsADC_Widget.py`

V1 split:
- Domain module for threshold-based ROI filtering and metric calculation.
- Service for pairing vMRE image, label, and sADC image inputs.
- UI may stay partial if needed, but the underlying calculation logic should be fully real and testable.

## Data Flow

### Single-file metric flow

1. User selects image and label.
2. UI creates a request object.
3. Service loads both NIfTI files.
4. Domain layer validates matching dimensions.
5. Domain layer computes metrics.
6. UI renders values and optional export uses the export service.

### Batch metric flow

1. User selects image and label folders.
2. Service pairs inputs deterministically.
3. Each pair is validated and processed.
4. Results are accumulated in a typed structure.
5. Export service writes a DataFrame to Excel.

## Error Handling

V1 should replace silent returns and loosely-scoped message boxes with explicit validation paths.

- Missing file/folder selection: user-visible validation message.
- Shape mismatch between image and label: structured domain error.
- Empty ROI: return explicit empty or null-safe result instead of accidental NaN propagation where possible.
- Invalid batch pairing: fail with a precise explanation.
- File overwrite behavior: explicit and consistent.

## Testing Strategy

V1 testing should prioritize the pure logic that is currently embedded in widgets.

### Unit tests

- Full-kidney ROI mean and volume calculation.
- Left/right split logic.
- Middle-slice ROI calculation.
- vMRE threshold filtering behavior.
- Filename extraction and folder traversal rules.
- Rename behavior.
- NIfTI extension conversion path logic.

### Fixture strategy

- Reuse a small subset of current test NIfTI files where useful.
- Add synthetic numpy-based fixtures for pure metric tests to reduce coupling to large sample files.

## Engineering Rules For V1

- Preserve baseline behavior before improving UX.
- Keep domain logic pure and independent from PyQt.
- Keep services thin and composable.
- Keep widgets small and declarative.
- Move generated outputs and caches out of the long-term tracked source layout after the v0 baseline is preserved.

## V1 Scope Boundaries

### In scope

- New package structure.
- New entrypoint organization.
- Extraction of reusable calculation and file services.
- Basic README and project metadata.
- Automated tests for core logic.
- Cleanup of obvious generated artifacts from the working tree after baseline preservation.

### Out of scope

- Large visual redesign.
- New algorithms beyond faithfully porting current workflows.
- Cloud sync, database support, or multi-user features.
- Major workflow invention.

## Risk Management

1. Preserve `v0-code-0` as the rollback point.
2. Port pure logic first and test it before reattaching UI.
3. Keep old workflows understandable while moving code in small steps.
4. Avoid simultaneous algorithm changes and UI redesign.

## Success Criteria

V1 is successful when:

- The repository has a clean, package-based structure.
- Core calculations are no longer embedded directly in widgets.
- The main workflows remain available from the desktop app.
- Core metric logic is covered by automated tests.
- The project is ready for a stronger v2 UX and product pass.
