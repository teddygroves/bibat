"""Dataclasses and functions for running bibat's command line wizard."""

from typing import Callable, Dict, List, Optional, Union

import click
from pydantic import root_validator
from pydantic.dataclasses import dataclass


@dataclass
class WizardStr:
    """A string field."""

    name: str
    prompt: str
    default: Union[str, Callable[[Dict], str]]


@dataclass
class WizardChoice:
    """A choice field."""

    name: str
    prompt: str
    options: List[str]
    default: Union[str, Callable[[Dict], str]]

    @root_validator
    def default_is_an_option(cls, values):
        """Check that the default is one of the options."""
        if isinstance(values["default"], str):
            msg = (
                f"default {values['default']} "
                f"not in options {values['options']}"
            )
            assert values["default"] in values["options"], msg
            return values


def prompt_user(
    wf: Union[WizardStr, WizardChoice], context: Optional[Dict]
) -> str:
    """Prompt the user for an input and parse it with click."""
    if context is not None and callable(wf.default):
        default = wf.default(context)
    elif isinstance(wf.default, str):
        default = wf.default
    else:
        raise ValueError("wf.default has unexpected type")
    if isinstance(wf, WizardStr):
        return click.prompt(wf.prompt, default=default, type=str)
    elif isinstance(wf, WizardChoice):
        return click.prompt(
            wf.prompt,
            default=wf.default,
            type=click.Choice(wf.options),
            show_choices=True,
        )
    else:
        raise ValueError(f"input {wf} is not a WizardStr or a WizardChoice")
