"""Unit tests for the cli module.

Adapted from examples here: https://click.palletsprojects.com/en/8.1.x/testing/

"""

import os
import shutil

from click.testing import CliRunner

from bibat.cli import generate_project


def test_generate_project():
    """Test that the generate_project function works when called normally."""
    runner = CliRunner()
    result = runner.invoke(generate_project)
    assert result.exit_code == 0
    shutil.rmtree("project_name")


def test_generate_project_with_config():
    """Test that the generate_project function works with a config file."""
    runner = CliRunner()
    f = os.path.join("tests", "data", "example_config.yml")
    result = runner.invoke(generate_project, ["--config-file", f])
    assert result.exit_code == 0
    shutil.rmtree("my_cool_project")
