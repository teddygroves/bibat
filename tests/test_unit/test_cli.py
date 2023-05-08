import os
import shutil

from click.testing import CliRunner

from bibat.cli import generate_project


def test_generate_project():
    runner = CliRunner()
    result = runner.invoke(generate_project)
    assert result.exit_code == 0
    shutil.rmtree("project_name")


def test_generate_project_with_config():
    runner = CliRunner()
    f = os.path.join("tests", "data", "example_config.yml")
    result = runner.invoke(generate_project, ["--config-file", f])
    assert result.exit_code == 0
    shutil.rmtree("my_cool_project")
