"""Dataclasses and functions for running bibat's command line wizard."""

import click
from pydantic.dataclasses import dataclass
from pydantic import root_validator
from typing import List, Union


@dataclass
class WizardFieldStr:
    """A string field."""

    name: str
    prompt: str
    default: str


@dataclass
class WizardFieldChoice:
    """A choice field."""

    name: str
    prompt: str
    options: List[str]
    default: str

    @root_validator
    def default_is_an_option(cls, values):
        """Check that the default is one of the options."""
        msg = f"default {values['default']} not in options {values['options']}"
        assert values["default"] in values["options"], msg
        return values


def prompt_user(wf: Union[WizardFieldStr, WizardFieldChoice]) -> str:
    """Prompt the user for an input and parse it with click."""
    if isinstance(wf, WizardFieldStr):
        return click.prompt(wf.prompt, default=wf.default, type=str)
    elif isinstance(wf, WizardFieldChoice):
        return click.prompt(
            wf.prompt,
            default=wf.default,
            type=click.Choice(wf.options),
            show_choices=True,
        )
    else:
        raise ValueError(
            f"input {wf} is not a WizardFieldStr or a WizardFieldChoice"
        )
