# Agent instructions

Follow [README.md](README.md) for setup, layout, notebook workflow, data handling, Git conventions and code checks.

Dependency add/remove/upgrade only when asked. New package needed -> say so -> wait for approval -> `uv add <pkg>` | `uv add --dev <pkg>`

## Permissions

- Default: user saves, exports, runs, commits
- Without asking: read project files, including notebooks/data, for context; read-only schemas + small samples
- Explicit request only: create/edit files; run notebook cells/scripts; write `data/processed/`; change `pyproject.toml`, dependencies, project config
- NEVER modify/move/delete `data/raw/` contents. Existing `data/processed/` overwrite -> confirmation required
- Responses: large dumps/sensitive values forbidden; schemas + few rows max

## Data Wrangler default

Unless user overrides: VS Code + Data Wrangler open on dataset; request == custom-operation snippet only. User pastes, previews, applies, saves, exports. Skip run-location/output-form questions

### Context

1. Read active VS Code editor, open tabs, selection first
2. Confirm actual columns, dtypes, prior cleaning steps; file reads/schema inspection always allowed
3. Open file absent | ambiguous context, including multiple candidate datasets/column mismatch -> one short question before code
4. Invented columns forbidden; referenced column absent -> state absence + suggest closest match

### Snippet contract

- Existing DataFrame `df` -> result in `df`; plain vectorized pandas
- Forbid `iterrows`, `inplace=True`, chained assignment; `apply(axis=1)` only when vectorized form absent
- One logical cleaning step/snippet; larger request -> separate snippets in apply order
- Self-contained; notebook-variable/earlier-cell dependencies forbidden
- `pd` only; other import truly needed -> snippet top + mention
- Explicitly handle `NaN`, `None`, empty strings + state treatment; idempotent
- Forbid load/save/export: `read_*`, `to_*`, file paths; function wrappers, `clean_data` definitions, `if __name__` blocks; output/preview: `print`, `display`, plots, `df.head()`
- Drop/rename/reorder of columns/rows only within request
- Unclear business rule -> most reasonable definition + state assumption + keep editable

## Notebook/code work on request

- Follow the shared notebook, output-naming and code conventions in `README.md`.
- Source stems collide: ask before a conflicting output write.
- Preserve existing cell outputs; restructure only within request scope.
- Run checks without executing notebook cells. Default: user runs cells.

## Git management

- Before staging notebooks: inspect saved outputs/embedded data for dataset contents/sensitive values; remove only when authorized; staging exposures forbidden.
- Default: user commits. Follow the shared Git conventions in `README.md` when asked to commit.

## Snippet output

1. Single paste-ready Python code block
2. One or two assumption lines: used columns, new column name, null handling, threshold
3. Nothing else unless explanation requested
