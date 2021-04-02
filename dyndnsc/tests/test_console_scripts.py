# -*- coding: utf-8 -*-

"""Tests for the console script using the pytest-console-scripts fixture."""

import pytest

# flake8: noqa


@pytest.mark.script_launch_mode('inprocess')
def test_version(script_runner):
    from dyndnsc import __version__
    ret = script_runner.run("dyndnsc", "--version")
    assert ret.success
    assert ret.stdout == "dyndnsc %s\n" % __version__
    assert ret.stderr == ""


@pytest.mark.script_launch_mode('inprocess')
def test_presets(script_runner):
    ret = script_runner.run("dyndnsc", "--list-presets")
    assert ret.success
    assert "updater-url" in ret.stdout
    assert ret.stderr == ""


@pytest.mark.script_launch_mode('inprocess')
def test_help(script_runner):
    ret = script_runner.run("dyndnsc", "--help")
    assert ret.success
    assert "usage: dyndnsc" in ret.stdout
    assert ret.stderr == ""


@pytest.mark.script_launch_mode('inprocess')
def test_null_dummy(script_runner):
    ret = script_runner.run(
        "dyndnsc",
        "--detector-null",
        "--updater-dummy",
        "--updater-dummy-hostname", "example.com"
    )
    assert ret.success
    assert ret.stdout == ""
    assert ret.stderr == ""


@pytest.mark.script_launch_mode('inprocess')
def test_null_dummy_debug(script_runner):
    ret = script_runner.run(
        "dyndnsc",
        "--detector-null",
        "--updater-dummy",
        "--updater-dummy-hostname", "example.com",
        "--debug"
    )
    assert ret.success
    assert ret.stdout == ""
    assert "DEBUG" in ret.stderr


@pytest.mark.script_launch_mode('inprocess')
def test_null_dummy_logjson(script_runner):
    ret = script_runner.run(
        "dyndnsc",
        "--detector-null",
        "--updater-dummy",
        "--updater-dummy-hostname", "example.com",
        "--log-json", "--debug"
    )
    assert ret.success
    assert "{\"written_at\":" in ret.stdout
    assert ret.stderr == ""
