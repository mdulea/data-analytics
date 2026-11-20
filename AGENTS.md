# Invariants

Follow [README.md](README.md) for setup, layout, notebooks, data handling, Git and checks.
Dependencies: add/remove/upgrade only when asked; new package needed -> notify -> await approval -> `uv add <pkg>` | `uv add --dev <pkg>`.

## Permissions

- Default: user saves, exports, runs, commits.
- Read project files, notebooks/data, schemas + small samples without asking.
- Explicit request required: create/edit files; run notebook cells/scripts; write `data/processed/`; change `pyproject.toml`, dependencies, project config.
- NEVER modify/move/delete `data/raw/` contents; overwrite existing `data/processed/` -> confirmation.
- Responses: forbidden large dumps/sensitive values; schemas + few rows max.

## Data Wrangler default

Unless overridden: VS Code + Data Wrangler open on dataset; return custom-operation snippet only. User pastes, previews, applies, saves, exports. Skip run-location/output-form questions.

### Context

1. Read active VS Code editor, tabs, selection first.
2. Confirm actual columns, dtypes, prior cleaning; file/schema reads always allowed.
3. Open file absent | ambiguous context, including multiple datasets/column mismatch -> one short question before code.
4. Invented columns forbidden; referenced column absent -> state absence + suggest closest match.

### Snippet contract

- Existing DataFrame `df` -> result `df`; plain vectorized pandas.
- Forbidden: `iterrows`, `inplace=True`, chained assignment; `apply(axis=1)` only without vectorized form.
- One cleaning step/snippet; larger request -> separate snippets in apply order.
- Self-contained; notebook-variable/earlier-cell dependencies forbidden.
- `pd` only; other import truly needed -> at top + mention.
- Explicitly handle `NaN`, `None`, empty strings; state treatment; idempotent.
- Forbidden: load/save/export: `read_*`, `to_*`, file paths; function wrappers, `clean_data` definitions, `if __name__` blocks; output/preview: `print`, `display`, plots, `df.head()`.
- Drop/rename/reorder rows/columns only within request.
- Unclear business rule -> most reasonable definition; state assumption; keep editable.

## Notebook/code work on request

- Follow `README.md` notebook, output-naming and code conventions.
- Every notebook DataFrame: `df`; use `df` for previews/subsequent operations.
- Source stems collide -> ask before conflicting output write.
- Preserve cell outputs; restructure only within request scope.
- Run checks without executing notebook cells; user runs cells by default.

## Git management

- Before staging notebooks: inspect saved outputs/embedded data for dataset contents/sensitive values; remove only when authorized; staging exposures forbidden.
- User commits by default; when asked, follow `README.md` Git conventions.

## Snippet output

1. Single paste-ready Python code block.
2. One or two assumption lines: used columns, new column name, null handling, threshold.
3. Nothing else unless explanation requested.
