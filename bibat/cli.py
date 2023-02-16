"""Cli for constructing the template.

I used this approach because I wanted to make longer prompts.
"""

import argparse
import os
from pathlib import Path

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
    WizardStr("author_name", "What is your name?", "Author name"),
    WizardStr("author_email", "What is your email?", "Author email"),
    WizardStr(
        "coc_contact",
        "Who should be the code of conduct contact?",
        "Code of conduct contact",
    ),
    WizardStr(
        "description",
        "Please briefly describe your project",
        "A short description of the project.",
    ),
    WizardChoice(
        "open_source_license",
        "Choose an open source license from these options:",
        ["MIT", "BSD-3-Clause", "No license file"],
        "MIT",
    ),
    WizardChoice(
        "docs_format",
        "How would you like to document your project?",
        ["Quarto", "Sphinx", "No docs"],
        "Quarto",
    ),
    WizardStr(
        "create_tests_directory",
        "Would you like to create a tests directory?",
        "y",
    ),
    WizardStr(
        "create_dotgithub_directory",
        "Would you like to create a .github directory?",
        "y",
    ),
    WizardStr(
        "install_python_tooling",
        "Would you like to install these handy Python tools?\n\t"
        + "\n\t".join(TOOLING_PACKAGES),
        "y",
    ),
]


def main():
    """Run bibat's cli."""
    parser = argparse.ArgumentParser(
        description="Generate a Bayesian statistical analysis project."
    )
    parser.add_argument(
        "--config-file",
        type=Path,
        default=None,
        help="path to a yaml file with prefilled cookiecutter fields",
    )
    args = parser.parse_args()
    config_file = args.config_file
    if config_file is not None:
        cookiecutter(THIS_DIR, no_input=True, config_file=config_file)
        return
    print("Welcome to the Batteries-Included Bayesian Analysis Template!")
    context = {wf.name: prompt_user(wf) for wf in WIZARD_FIELDS}
    context["repo_name"] = context["project_name"].lower().replace(" ", "_")
    context["bibat_version"] = bibat_version
    cookiecutter(
        THIS_DIR, no_input=True, extra_context=context, config_file=config_file
    )


if __name__ == "__main__":
    main()
