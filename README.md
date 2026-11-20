# Data analytics invariants

Jupyter workspace: pandas + VS Code Data Wrangler for tabular exploration/cleaning; synthetic data modeled on real datasets. Setup first, then copy notebook template before source analysis.

## Setup

uv manages Python/dependencies; project root contains `pyproject.toml`.

### Install uv

Check `uv --version`; installed -> skip OS installer.

#### Windows

PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart terminal. Install VS Code if needed; enable installer option adding `code` to PATH.

#### macOS

Terminal:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart terminal. Install VS Code if needed; View -> Command Palette -> "Shell Command: Install 'code' command in PATH". Restart terminal.

### Shared setup

Windows/macOS, from project root; commands as written:

```sh
uv --version
code --install-extension ms-toolsai.jupyter
code --install-extension ms-toolsai.datawrangler
uv sync --locked
code .
```

Python 3.12+ required. Each notebook kernel picker: choose `.venv` Python environment for cell execution. Python programs: `uv run <command>`. `pip`, manual environment activation and hand edits to `uv.lock` forbidden; uv manages lock.

### New project only

New project without `pyproject.toml` -> commands here; existing checkouts -> shared setup.

```sh
uv init --bare --vcs none --no-package --description "Add your description here"
uv python pin 3.12
uv add --dev ruff pyright pandas-stubs
uv add duckdb ipykernel jupyter openpyxl pandas pyarrow python-calamine sdv
```

## Notebook workflow

Templates in `notebooks/`:

- `convert.ipynb`: CSV/selected Excel sheet -> string-valued `data/raw/parquet/`.
- `explore.ipynb`: discover CSV/Parquet/Excel tables; inspect column types, missing values, distinct counts.
- `transform.ipynb`: raw Parquet -> `df` -> Data Wrangler transformations -> optional cleaned Parquet save.
- `export.ipynb`: processed Parquet -> `.xlsx` data/source-schema sheets.
- `synthetic.ipynb`: SDV synthetic tabular data.

Before source-specific edits, copy template to `notebooks/explorations/<raw-stem>.ipynb`. Stem = filename minus extension; preserve case, spaces, punctuation. Cross-extension matching stems -> `example.xlsx.ipynb`, `example.csv.ipynb`.

Inspect original with `explore.ipynb` before conversion. `convert.ipynb`: CSV/Excel -> `data/raw/parquet/<raw-stem>.parquet`; save creates folder. `dtype=str` + `keep_default_na=False` preserve text identifiers, empty strings, null markers for later cleaning. Excel display formatting lost; one sheet/conversion. Existing outputs block writes, including matching stems across sources/sheets.

Copy `transform.ipynb` to exploration notebook; select raw Parquet sibling in `data/raw/parquet/`. Export Data Wrangler steps to transformation cell; result `df`; convert types after raw conversion. After cleaning, optional final save creates folder and writes `data/processed/<raw-stem>.parquet` with transformed types, without index; existing outputs blocked. Loading/transforming `df` leaves source unchanged.

`export.ipynb` -> `data/exports/<raw-stem>.xlsx`:

- `data`: values without DataFrame index.
- `data_types`: `column_name`, `parquet_type` directly from source Parquet schema.
- Excel precision: long integers, exact decimals, some floats as text; dates/times/timestamps/durations as text; missing values as blank cells.
- Unsupported values/Excel size limits stop export; existing exports blocked. Retain processed Parquet for analysis with original schema.

Set source path in copy. CSV/Parquet: one table. Excel: select sheet; keep all selected sheets from one source in same notebook. Data Wrangler: paste cleaning -> preview against data -> apply -> export edits to same notebook copy. Keep templates reusable. Every DataFrame preview uses `df`; later previews replace current `df`, including `explore.ipynb` column profile.

## Data and paths

- `data/raw/`: sources; NEVER modify/move/delete existing files during analysis.
- `data/raw/parquet/`: user-saved raw conversions; existing outputs blocked.
- `data/processed/`: user-saved cleaned Parquet.
- `data/exports/`: processed Parquet Excel delivery copies + source schema sheets.
- `data/synthetic/`: labeled SDV synthetic datasets.

Paths relative to project root; read sources from `data/raw/`; cleaned output `data/processed/<raw-stem>.parquet`. Replace extension only; preserve exact stem. Sheet names, dates, suffixes such as `_clean` forbidden. Resolve matching stems before conflicting writes; confirm existing processed overwrite.

Excel reads: `pd.read_excel(path, engine="calamine")`; Excel writes: `openpyxl`; Parquet: `pyarrow`. DuckDB: large file/DataFrame queries or clearer SQL. SDV: synthetic generation only.

## Contributing

Track notebooks, reusable code, docs; under `data/`, only empty `.gitkeep` placeholders. Force-adding ignored files forbidden. Exclude credentials, local environments, generated files, unrelated changes.

Before notebook staging: inspect saved outputs/embedded data for dataset contents/sensitive values; staging exposed data forbidden. Stage explicit paths; review staged diff before committing.

Branches: `<type>/<short-purpose>`, lowercase hyphen-separated words. Commit subjects: `<type>: <reason>`; types `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`. Explain why; one purpose/commit; optional body for motivation, constraints, tradeoffs.

### Code conventions

Python 3.12 syntax; function type hints; `snake_case` variables/new columns. Small, single-purpose notebook cells; imports in first code cell. Restructuring: preserve outputs; changes within request scope.

Python/notebook docstrings forbidden. `#` comments only for decisions/reasons unexplained by code/filenames. Prefer explicit column selection, clear boolean masks.

Before committing: run appropriate checks. Python/notebook changes require all three:

```sh
uv run ruff format
uv run ruff check
uv run python scripts/typecheck.py
```

Type checker: strict Pyright settings from `pyproject.toml`; notebooks checked via temporary Python files with cell-number diagnostic comments; cells unexecuted.

## Dependencies and agent output

- `duckdb`: SQL queries over files/DataFrames.
- `ipykernel`: notebook Python execution.
- `jupyter`: interactive notebook tools.
- `openpyxl`: Excel `.xlsx` reads/writes.
- `pandas`: DataFrame cleaning/transformation/analysis.
- `pyarrow`: Arrow in-memory columns; column-based Parquet reads/writes.
- `python-calamine`: Excel/OpenDocument reads.
- `sdv`: synthetic tabular data from real datasets.

Development: Ruff formatting/code rules; Pyright type checks; `pandas-stubs` pandas type definitions. [AGENTS.md](AGENTS.md): agent permissions + cleaning snippet contract.
