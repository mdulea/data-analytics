# Data analytics

A Jupyter workspace for exploring and cleaning tabular data with pandas and VS Code Data Wrangler. It also generates synthetic data modeled on real datasets. Follow the setup below, then copy a notebook template before analyzing a source file.

## Setup

uv manages the project's Python environment and dependencies. The project root is the directory containing `pyproject.toml`.

### 1. Install uv

Run `uv --version`. If uv is installed, skip the installer for your operating system.

#### Windows

Run in PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart the terminal. Install VS Code if needed and enable its installer's option to add `code` to PATH so the terminal can find the command.

#### macOS

Run in Terminal:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart the terminal. Install VS Code if needed. Open its Command Palette from the View menu and run "Shell Command: Install 'code' command in PATH" so the terminal can find `code`. Restart the terminal.

### 2. Run shared setup commands

Run these commands from the project root on Windows or macOS:

```sh
uv --version
code --install-extension ms-toolsai.jupyter
code --install-extension ms-toolsai.datawrangler
uv sync --locked
code .
```

In each notebook's kernel picker, choose the Python environment in `.venv` to execute its cells. Python 3.12 or later is required. Execute Python programs through `uv run <command>`. Run the displayed setup commands as written. Do not use `pip` or activate the environment manually. Let uv manage `uv.lock`; do not edit it by hand.

### Create a project from scratch

Use these commands only when creating a new project without `pyproject.toml`. Existing checkouts use the shared setup above.

```sh
uv init --bare --vcs none --no-package --description "Add your description here"
uv python pin 3.12
uv add --dev ruff pyright pandas-stubs
uv add duckdb ipykernel jupyter openpyxl pandas pyarrow python-calamine sdv
```

## Notebook workflow

The templates in `notebooks/` have separate purposes:

| Template | Purpose |
| --- | --- |
| `explore.ipynb` | Discover tables in CSV, Parquet or Excel files and inspect column types, missing values and distinct counts. |
| `transform.ipynb` | Load CSV, Parquet or Excel data into a DataFrame named `df` before cleaning. |
| `synthetic.ipynb` | Generate synthetic tabular data with SDV. |

Copy a template to `notebooks/explorations/<raw-stem>.ipynb` before changes for a particular source. The source stem is its filename without the extension. Preserve its case, spaces and punctuation. If source stems match across extensions, use names such as `example.xlsx.ipynb` and `example.csv.ipynb`.

Set the source path in the copy. CSV and Parquet files hold one table. For Excel files, set the selected sheet and keep all selected sheets from one source file in the same notebook. Paste cleaning operations into Data Wrangler, preview them against the data, then apply them. Export Data Wrangler edits to that same notebook copy. Keep the templates reusable. Each DataFrame preview uses `df`. Later preview cells replace the current `df`, including the column profile in `explore.ipynb`.

## Data and paths

| Directory | Contents |
| --- | --- |
| `data/raw/` | Read-only source files. Never modify, move or delete them as part of analysis. |
| `data/processed/` | Cleaned Parquet outputs saved by the user. |
| `data/synthetic/` | Labeled synthetic datasets from SDV. |

Use paths relative to the project root. Read source data from `data/raw/`. Save cleaned data as `data/processed/<raw-stem>.parquet`. Replace only the source extension and preserve the exact stem. Do not append sheet names, dates or suffixes such as `_clean`. Resolve matching source stems before writing conflicting outputs. Confirm before overwriting an existing processed file.

For Excel reads, use `pd.read_excel(path, engine="calamine")`. Use `openpyxl` for Excel writes and `pyarrow` for Parquet. Use DuckDB for large file or DataFrame queries, or when SQL is clearer. Use SDV only for synthetic generation.

## Contributing

Track notebooks, reusable code and documentation. Under `data/`, track only empty `.gitkeep` placeholders. Never force-add ignored files. Exclude credentials, local environments, generated files and unrelated changes.

Before staging a notebook, inspect its saved outputs and embedded data for dataset contents or sensitive values. Do not stage exposed data. Stage explicit paths and review the staged diff before committing.

Use branches named `<type>/<short-purpose>` with lowercase, hyphen-separated words. Use commit subjects of the form `<type>: <reason>`. Allowed types are `feat`, `fix`, `refactor`, `docs`, `test`, `chore` and `perf`. Explain why the change is needed. Keep one purpose per commit; use an optional body for motivation, constraints or tradeoffs.

### Code conventions

Use Python 3.12 syntax, type hints on functions and `snake_case` for variables and new columns. Keep notebook cells small and single-purpose, with imports in the first code cell. When restructuring notebooks, preserve existing cell outputs and limit changes to the requested scope.

Do not write Python or notebook code docstrings. Use `#` comments only for decisions or reasons that the code and filenames do not explain. Prefer explicit column selection and clear boolean masks.

Run appropriate checks before committing. Python and notebook changes require all three commands:

```sh
uv run ruff format
uv run ruff check
uv run python scripts/typecheck.py
```

The type checker uses strict Pyright settings from `pyproject.toml`. It checks notebook code through temporary Python files with cell-number comments for diagnostics. It does not execute notebook cells.

## Dependencies

| Package | Purpose |
| --- | --- |
| `duckdb` | SQL queries over files and DataFrames. |
| `ipykernel` | Python execution in notebook kernels. |
| `jupyter` | Interactive notebook tools. |
| `openpyxl` | Excel `.xlsx` reading and writing. |
| `pandas` | DataFrame cleaning, transformation and analysis. |
| `pyarrow` | Arrow data held in memory by column, and reading and writing the column-based Parquet file format. |
| `python-calamine` | Excel and OpenDocument spreadsheet reading. |
| `sdv` | Synthetic tabular data generation from real datasets. |

Development tools are Ruff for formatting and checking code rules, Pyright for type checks, and `pandas-stubs` for pandas type definitions. [AGENTS.md](AGENTS.md) contains agent permissions and the cleaning snippet contract.
