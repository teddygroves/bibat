"""Unit tests for the copier template."""

from pathlib import Path
from tempfile import TemporaryDirectory

import copier

HERE = Path(__file__).parent
EXAMPLE_DATA = {
    "project_name": "My Cool Project",
    "project_name_no_spaces": "my_cool_project",
    "description": "bla bla bla",
    "author_name": "Author",
    "author_email": "author@email.com",
    "coc_contact": "author@email.com",
    "open_source_license": "MIT",
    "docs_format": "Quarto",
    "create_dotgithub_directory": True,
}


def test_copier_runs() -> None:
    """Test that copier runs."""
    source = HERE / ".." / ".." / "template"
    with TemporaryDirectory() as destination:
        copier.run_copy(str(source), destination, data=EXAMPLE_DATA)
