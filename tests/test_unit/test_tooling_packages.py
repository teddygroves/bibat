"""Check that the tooling packages in the cli match those in the template."""

import os

from bibat.cli import TOOLING_PACKAGES as from_cli

TOOLING_PACKAGE_FILE = os.path.join(
    "bibat", "{{cookiecutter.repo_name}}", "requirements-tooling.txt"
)


def test_tooling_packages():
    """Check that the tooling packages in the cli match the template."""
    with open(TOOLING_PACKAGE_FILE, "r") as f:
        from_txt = f.readlines()
    for p_from_txt, p_from_cli in zip(from_txt, from_cli):
        assert p_from_txt.strip() == p_from_cli
