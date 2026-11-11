import ast
import json
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING, Literal

# Share SDV types with Pylance because SDV 2.2 has no published types.
if TYPE_CHECKING:
    import pandas as pd

    class Metadata:
        @classmethod
        def detect_from_dataframes(
            cls,
            data: dict[str, pd.DataFrame],
            *,
            infer_keys: Literal["primary_and_foreign", "primary_only"]
            | None = "primary_and_foreign",
        ) -> "Metadata":
            raise NotImplementedError

        def save_to_json(
            self, filepath: str, mode: Literal["write", "overwrite"] = "write"
        ) -> None:
            raise NotImplementedError

        def get_column_names(self, **kwargs: str | bool) -> list[str]:
            raise NotImplementedError

        def update_column(self, column_name: str, **kwargs: str | bool) -> None:
            raise NotImplementedError

    class GaussianCopulaSynthesizer:
        def __init__(self, metadata: Metadata) -> None:
            raise NotImplementedError

        def fit(self, data: dict[str, pd.DataFrame]) -> None:
            raise NotImplementedError

        def sample(self, num_rows: int) -> dict[str, pd.DataFrame]:
            raise NotImplementedError


def notebook_source(source: str) -> str:
    statements = ast.parse(source).body
    if statements and isinstance(statements[-1], ast.Expr):
        # Notebook display values would otherwise trigger unused-expression errors.
        lines = source.splitlines(keepends=True)
        lines[statements[-1].lineno - 1] = "_ = " + lines[statements[-1].lineno - 1]
        return "".join(lines)
    return source


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    with TemporaryDirectory(prefix="notebook-typecheck-") as directory:
        notebook_files: list[str] = []
        for notebook in sorted((root / "notebooks").rglob("*.ipynb")):
            target = Path(directory) / notebook.relative_to(root).with_suffix(".py")
            target.parent.mkdir(parents=True, exist_ok=True)
            cells = json.loads(notebook.read_text(encoding="utf-8"))["cells"]
            target.write_text(
                "\n\n".join(
                    f"# Notebook cell {number}\n{notebook_source(''.join(cell['source']))}"
                    for number, cell in enumerate(cells, start=1)
                    if cell["cell_type"] == "code"
                ),
                encoding="utf-8",
            )
            notebook_files.append(str(target))
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "pyright",
                "--project",
                str(root),
                str(root),
                *notebook_files,
            ],
            cwd=root,
            check=False,
        ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
