"""Cli for constructing the template.

I used this approach because I wanted to make longer prompts.
"""
import os

from typing import List, Union

from cookiecutter.main import cookiecutter

PARENT = os.path.dirname(os.path.dirname(__file__))
FIELD_TO_PROMPT_AND_DEFAULT = {
    "project_name": (
        "What would you like your project to be called?", "project_name"
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
        "Would you like to create a tests directory?", "y"
    ),
    "create_dotgithub_directory": (
        "Would you like to create a .github directory?", "y"
    )
}


def input_with_default(prompt: str, options: Union[str, List]):
    def i_to_str(i):
        return str(i+1) if i > 0 else f"[{str(i+1)}]"
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
    print("Welcome to the medium-sized Bayesian analysis generator!")
    context = {
        field: input_with_default(prompt, default)
        for field, (prompt, default) in FIELD_TO_PROMPT_AND_DEFAULT.items()
    }
    context["repo_name"] = context["project_name"].lower().replace(" ", "_")
    cookiecutter(PARENT, extra_context=context)


if __name__ == "__main__":
    main()
