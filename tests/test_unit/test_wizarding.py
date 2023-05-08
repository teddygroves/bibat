"""Test the wizarding module."""

import click
import pytest
from click.testing import CliRunner

from bibat.wizarding import WizardChoice, WizardStr, prompt_user


def test_wizard_str_good():
    """Test that the WizardStr class instantiates as expected."""
    WizardStr("name", "What's your name?", "Sasha")


def test_wizard_choice_good():
    """Test that the WizardChoice class instantiates as expected."""
    WizardChoice("name", "What's your name?", ["Sasha", "Alex"], "Sasha")


@pytest.mark.xfail
def test_wizard_choice_bad():
    """Test that the WizardChoice class fails as expected."""
    WizardChoice("name", "What's your name?", ["Sasha", "Alex"], "Lex")


def test_prompt_user_good():
    """Test that the prompt_user function works as expected."""
    runner = CliRunner()
    c = WizardChoice("name", "What's your name?", ["Sasha", "Alex"], "Sasha")

    @click.command()
    def prompt_c():
        return prompt_user(c)

    runner.invoke(prompt_c, input="Alex")


@pytest.mark.xfail
def test_prompt_user_bad():
    """Test that the prompt_user function fails as expected."""
    runner = CliRunner()
    c = "asdfasdf"

    @click.command()
    def prompt_c():
        return prompt_user(c)

    runner.invoke(prompt_c, input="Alex")


@pytest.mark.xfail
def test_prompt_user_bad_input():
    """Test that the prompt_user function fails with incorrect default."""
    prompt_user(123, context=None)
