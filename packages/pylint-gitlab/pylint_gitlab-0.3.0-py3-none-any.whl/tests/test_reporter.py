#
# Copyright 2019 Stephan Müller
#
# Licensed under the MIT license

"""Tests for ``pylint_gitlab.reporter``."""

import json
import os
from io import StringIO

import pytest
from pylint.lint import PyLinter


@pytest.mark.parametrize("use_load_plugins", [False, True])
def test_gitlab_pages_html_reporter(use_load_plugins):
    """Tests for ``pylint_gitlab.reporter.GitlabPagesHtmlReporter()``."""

    if use_load_plugins:
        plugins = ["pylint_gitlab"]
        reporter = "gitlab-pages-html"
    else:
        plugins = []
        reporter = "pylint_gitlab.GitlabPagesHtmlReporter"

    output = StringIO()
    linter = PyLinter()

    linter.load_plugin_modules(plugins)
    linter.set_option("output-format", reporter)
    linter.set_option("persistent", False)
    linter.load_default_plugins()

    reporter = linter.reporter
    reporter.set_output(output)
    reporter.CI_PROJECT_URL = "https://example.org"
    reporter.CI_COMMIT_REF_NAME = "branch"

    linter.open()

    linter.set_current_module("b")
    linter.add_message("line-too-long", line=2, args=(1, 2))
    linter.add_message("line-too-long", line=1, args=(1, 2))

    linter.set_current_module("a")
    linter.add_message("line-too-long", line=1, args=(1, 2))

    # we call this method because we didn't actually run the checkers
    reporter.display_messages(None)

    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "report.html"), "r") as file:
        expected_result = file.read()
    assert output.getvalue() == expected_result


@pytest.mark.parametrize("use_load_plugins", [False, True])
def test_gitlab_code_climate_reporter(use_load_plugins):
    """Tests for ``pylint_gitlab.reporter.GitlabCodeClimateReporter()``."""

    if use_load_plugins:
        plugins = ["pylint_gitlab"]
        reporter = "gitlab-codeclimate"
    else:
        plugins = []
        reporter = "pylint_gitlab.GitlabCodeClimateReporter"

    output = StringIO()
    linter = PyLinter()

    linter.load_plugin_modules(plugins)
    linter.set_option("output-format", reporter)
    linter.set_option("persistent", False)
    linter.load_default_plugins()

    reporter = linter.reporter
    reporter.set_output(output)

    linter.open()

    linter.set_current_module("0123")
    linter.add_message("line-too-long", line=1, args=(1, 2))

    # we call this method because we didn't actually run the checkers
    reporter.display_messages(None)

    expected_result = [{
        "description": "C0301: Line too long (1/2)",
        "severity": "minor",
        "location": {
            "path": "0123",
            "lines": {
                "begin": 1,
            }
        },
        "fingerprint": "21e7b7887a841a99f73b9cf1771bf387"
    }]
    report_result = json.loads(output.getvalue())
    assert report_result == expected_result
