"""Cli for constructing the template.

I used this approach because I wanted to make longer prompts.
"""

import os

import click
from cookiecutter.main import cookiecutter

from bibat import __version__ as bibat_version
from bibat.wizarding import WizardChoice, WizardStr, prompt_user

THIS_DIR = os.path.dirname(__file__)
TOOLING_PACKAGES = [
    "pandas-stubs",
    "types-toml",
    "flake8",
    "flake8-bugbear",
    "flake8-docstrings",
    "mypy",
    "python-lsp-server[all]",
    "python-lsp-black",
    "pylsp-mypy",
    "pyls-isort",
]

WIZARD_FIELDS = [
    WizardStr("project_name", "What is your project called?", "Project Name"),
    WizardStr(
        "repo_name",
        "What should the project repository be called",
        default_function=lambda context: context["project_name"]
        .lower()
        .replace(" ", "_"),
    ),
    WizardStr("author_name", "What is your name?", default="Author name"),
    WizardStr("author_email", "What is your email?", default="Author email"),
    WizardStr(
        "coc_contact",
        "Who should be the code of conduct contact?",
        default_function=lambda context: context["author_email"],
    ),
    WizardStr(
        "description",
        "Please briefly describe your project",
        default="A short description of the project.",
    ),
    WizardChoice(
        "open_source_license",
        "Choose an open source license from these options:",
        ["MIT", "BSD-3-Clause", "No license file"],
        default="MIT",
    ),
    WizardChoice(
        "docs_format",
        "How would you like to document your project?",
        ["Quarto", "Sphinx", "No docs"],
        default="Quarto",
    ),
    WizardStr(
        "create_tests_directory",
        "Would you like to create a tests directory?",
        default="y",
    ),
    WizardStr(
        "create_dotgithub_directory",
        "Would you like to create a .github directory?",
        default="y",
    ),
    WizardStr(
        "install_python_tooling",
        "Would you like to install these handy Python tools?\n\t"
        + "\n\t".join(TOOLING_PACKAGES),
        default="y",
    ),
]


@click.command()
@click.option(
    "--config-file",
    type=click.Path(exists=True),
    default=None,
    help="Path to a yaml file with prefilled cookiecutter fields.",
)
def main(config_file):
    """Generate a Bayesian statistical analysis project."""
    if config_file is not None:
        cookiecutter(THIS_DIR, no_input=True, config_file=config_file)
        return
    click.echo("Welcome to the Batteries-Included Bayesian Analysis Template!")
    context = {}
    for wizard_field in WIZARD_FIELDS:
        context[wizard_field.name] = prompt_user(wizard_field, context)
    context["bibat_version"] = bibat_version
    cookiecutter(
        THIS_DIR, no_input=True, extra_context=context, config_file=config_file
    )


if __name__ == "__main__":
    main()
