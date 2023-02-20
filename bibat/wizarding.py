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
    default: Optional[str] = None
    default_function: Optional[Callable] = None

    @root_validator
    def default_or_default_function_exists(cls, values):
        """Either the default or the default function must not be None."""
        assert (values["default"] is not None) or (
            values["default_function"] is not None
        ), "Either the default or the default function must not be None."
        return values


@dataclass
class WizardChoice:
    """A choice field."""

    name: str
    prompt: str
    options: List[str]
    default: Optional[str] = None
    default_function: Optional[Callable] = None

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

    @root_validator
    def default_or_default_function_exists(cls, values):
        """Either the default or the default function must not be None."""
        assert (values["default"] is not None) or (
            values["default_function"] is not None
        ), "Either the default or the default function must not be None."
        return values


def prompt_user(
    wf: Union[WizardStr, WizardChoice], context: Optional[Dict]
) -> str:
    """Prompt the user for an input and parse it with click."""
    if context is not None and wf.default_function is not None:
        default = wf.default_function(context)
    elif isinstance(wf.default, str):
        default = wf.default
    else:
        raise ValueError(f"wf.default has unexpected type {type(wf.default)}")
    if isinstance(wf, WizardStr):
        return click.prompt(wf.prompt, default=default, type=str)
    elif isinstance(wf, WizardChoice):
        return click.prompt(
            wf.prompt,
            default=default,
            type=click.Choice(wf.options),
            show_choices=True,
        )
    else:
        raise ValueError(f"input {wf} is not a WizardStr or a WizardChoice")
