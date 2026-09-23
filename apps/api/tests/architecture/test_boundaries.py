"""Runs the import-linter contracts from pyproject.toml as part of the test suite."""

import subprocess
import sys
from pathlib import Path

import pytest

API_ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.architecture
def test_import_contracts_are_kept() -> None:
    result = subprocess.run(  # noqa: S603
        [str(Path(sys.executable).with_name("lint-imports")), "--config", "pyproject.toml"],
        cwd=API_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
