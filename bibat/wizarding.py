"""Dataclasses and functions for running bibat's command line wizard."""

from typing import Callable, Dict, List, Optional, Union

import click
from pydantic import model_validator
from pydantic.dataclasses import dataclass


@dataclass
class WizardStr:
    """A wizard question where the answer is a string.

    :param name: name of the field
    :param prompt: string that the user will be prompted with
    :param default: default answer
    :param default_function: function that returns a default answer, given a
        dictionary.
    """

    name: str
    prompt: str
    default: Optional[str] = None
    default_function: Optional[Callable] = None

    @model_validator(mode="after")
    def default_or_default_function_exists(cls, m: "WizardStr"):
        """Either the default or the default function must not be None."""
        assert (m.default is not None) or (
            m.default_function is not None
        ), "Either the default or the default function must not be None."
        return m


@dataclass
class WizardChoice:
    """A wizard question where the answer comes from a list of choices.

    :param name: name of the field
    :param prompt: string that the user will be prompted with
    :param default: default answer
    :param default_function: function that returns a default answer, given a
        dictionary.
    """

    name: str
    prompt: str
    options: List[str]
    default: Optional[str] = None
    default_function: Optional[Callable] = None

    @model_validator(mode="after")
    def default_is_an_option(cls, m: "WizardChoice"):
        """Check that the default is one of the options."""
        if isinstance(m.default, str):
            msg = f"default {m.default} not in options {m.options}"
            assert m.default in m.options, msg
            return m

    @model_validator(mode="after")
    def default_or_default_function_exists(cls, m: "WizardChoice"):
        """Either the default or the default function must not be None."""
        assert (m.default is not None) or (
            m.default_function is not None
        ), "Either the default or the default function must not be None."
        return m


def prompt_user(
    wq: Union[WizardStr, WizardChoice], context: Optional[Dict]
) -> str:
    """Prompt the user for an input and parse it with click.

    :param wq: A wizard question: should be one of the classes defined in the
        module wizarding.py.
    :param context: an optional dictionary containing the answers to previous
        prompts.
    """
    if not (isinstance(wq, WizardStr) or isinstance(wq, WizardChoice)):
        raise ValueError(f"input {wq} is not a WizardStr or a WizardChoice")
    if context is not None and wq.default_function is not None:
        default = wq.default_function(context)
    elif isinstance(wq.default, str):
        default = wq.default
    if isinstance(wq, WizardStr):
        return click.prompt(wq.prompt, default=default, type=str)
    elif isinstance(wq, WizardChoice):
        return click.prompt(
            wq.prompt,
            default=default,
            type=click.Choice(wq.options),
            show_choices=True,
        )
