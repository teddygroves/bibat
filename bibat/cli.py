"""Cli for constructing the template.

I used this approach because I wanted to make longer prompts.
"""

import argparse
import os
from pathlib import Path
from typing import List, Union

from cookiecutter.main import cookiecutter

from bibat import __version__ as bibat_version

PARENT = os.path.dirname(os.path.dirname(__file__))
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
FIELD_TO_PROMPT_AND_DEFAULT = {
    "project_name": (
        "What would you like your project to be called?",
        "project_name",
    ),
    "author_name": ("What is your name?", "Author name"),
    "author_email": ("What is your email?", "Author email"),
    "coc_contact": (
        "Who should be the code of conduct contact?",
        "Code of conduct contact",
    ),
    "description": (
        "Please briefly describe your project",
        "A short description of the project.",
    ),
    "open_source_license": (
        "Choose an open source license",
        ["MIT", "BSD-3-Clause", "No license file"],
    ),
    "docs_format": (
        "How would you like to document your project?",
        ["Markdown", "Sphinx", "No docs"],
    ),
    "create_tests_directory": (
        "Would you like to create a tests directory?",
        "y",
    ),
    "create_dotgithub_directory": (
        "Would you like to create a .github directory?",
        "y",
    ),
    "install_python_tooling": (
        "Would you like to install these handy Python tools?\n\t"
        + "\n\t".join(TOOLING_PACKAGES),
        "y",
    ),
}


def input_with_default(prompt: str, options: Union[str, List]):
    """Get a user input if provided, otherwise return a default."""

    def i_to_str(i):
        return str(i + 1) if i > 0 else f"[{str(i+1)}]"

    if isinstance(options, List):
        option_lines = [f"{o} - {i_to_str(i)}" for i, o in enumerate(options)]
        option_lines[0] = option_lines[0]
        prompt += "\n\t" + "\n\t".join(option_lines) + " "
        default = options[0]
    else:
        prompt += f" [{options}] "
        default = options
    user_input = input(prompt)
    return user_input if user_input != "" else default


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
        cookiecutter(PARENT, no_input=True, config_file=config_file)
        return
    print("Welcome to the Batteries-Included Bayesian Analysis Template!")
    context = {
        field: input_with_default(prompt, default)
        for field, (prompt, default) in FIELD_TO_PROMPT_AND_DEFAULT.items()
    }
    context["repo_name"] = context["project_name"].lower().replace(" ", "_")
    context["bibat_version"] = bibat_version
    cookiecutter(
        PARENT, no_input=True, extra_context=context, config_file=config_file
    )


if __name__ == "__main__":
    main()
