# tests/test_conf.py

import os

import pytest

from viz.conf import Conf


def test_conf_init():
    # Test that Conf initializes correctly with default values
    conf = Conf({"debug": False, "timeout": 10})
    assert conf.debug == False
    assert conf.timeout == 10


def test_conf_true_env_override():
    # Test that Conf use env variable
    os.environ["CONF_DUMMY123"] = "20"
    conf = Conf({"dummy123": 14})
    assert conf.dummy123 == 20
    del os.environ["CONF_DUMMY123"]


def test_conf_override_with_env_vars():
    conf = Conf(
        {"debug": False, "timeout": 10, "appname": "boulettes"},
        environ={
            "CONF_DEBUG": "True",
            "CONF_TIMEOUT": "20",
            "CONF_APPNAME": "couscous",
        },
    )
    assert conf.debug == True
    assert conf.timeout == 20
    assert conf.appname == "couscous"


def test_conf_override_with_kwargs():
    # Test that Conf overrides default values with keyword arguments
    conf = Conf(
        {"debug": False, "timeout": 10},
        environ={
            "CONF_DEBUG": "False",
            "CONF_TIMEOUT": "15",
        },
        debug=True,
        timeout=20,
    )
    assert conf.debug == True
    assert conf.timeout == 20


def test_conf_required_default_values():
    # Test that Conf raises an error if default_values is empty
    with pytest.raises(ValueError):
        Conf({})


def test_conf_type_conversion():
    # Test that Conf converts environment variable values to the correct type
    conf = Conf(
        {"foo": False, "bar": 0},
        environ={
            "CONF_FOO": "True",
            "CONF_BAR": "42",
        },
    )
    assert conf.foo == True
    assert conf.bar == 42


def test_conf_ignores_unknown_env_vars():
    # Test that Conf ignores environment variables that are not in default_values
    os.environ["CONF_UNKNOWN"] = "Hello"
    conf = Conf({"debug": False, "timeout": 10})
    assert not hasattr(conf, "unknown")
