import datetime
import os
import shlex
import subprocess
import sys
from contextlib import contextmanager

import pytest
from cookiecutter.utils import rmtree


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        rmtree(str(result.project))


def run_inside_dir(command, dirpath):
    """
    Run a command from inside a given directory, returning the exit status
    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))


def check_output_inside_dir(command, dirpath):
    """
    Run a command from inside a given directory, returning the command output
    """
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def test_year_compute_in_license_file(cookies):
    with bake_in_temp_dir(cookies) as result:
        license_file_path = result.project.join("LICENSE")
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read()


def project_info(result):
    """Get toplevel dir, project_slug, and project dir from baked cookies"""
    project_path = str(result.project)
    project_slug = os.path.split(project_path)[-1]
    project_dir = os.path.join(project_path, project_slug)
    return project_path, project_slug, project_dir


def test_bake_with_defaults(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert result.project.isdir()
        assert result.exit_code == 0
        assert result.exception is None

        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "pyproject.toml" in found_toplevel_files
        assert "python_boilerplate" in found_toplevel_files
        assert "tox.ini" in found_toplevel_files
        assert "tests" in found_toplevel_files


@pytest.mark.parametrize(
    "extra_context",
    [
        {},
        {
            "full_name": 'name "quote" name',
            "email": "name.quote.name@example.com",
            "github_username": "name-quote-name",
        },
        {
            "full_name": "O'connor",
            "email": "o.conner@example.com",
            "github_username": "o-conner",
        },
    ],
)
def test_bake_and_run_tests(cookies, extra_context):
    with bake_in_temp_dir(cookies, extra_context=extra_context) as result:
        assert result.project.isdir()
        assert run_inside_dir("poetry install", str(result.project)) == 0
        assert run_inside_dir("poetry run pytest", str(result.project)) == 0
        print("test_bake_and_run_tests path", str(result.project))


def test_bake_without_pypi_setup(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={"pypi_deployment": "n"},
    ) as result:
        assert "Release" not in result.project.join("README.rst").read()

        github_workflow_path = result.project.join(".github", "workflows")
        github_workflow_files = [f.basename for f in github_workflow_path.listdir()]
        assert "upload-python-package.yml" not in github_workflow_files

        docs_path = result.project.join("docs")
        docs_files = [f.basename for f in docs_path.listdir()]
        assert "pypi_release_checklist.rst" not in docs_files
        assert "pypi_release_checklist" not in docs_path.join("index.rst").read()


def test_make_help(cookies):
    with bake_in_temp_dir(cookies) as result:
        # The supplied Makefile does not support win32
        if sys.platform != "win32":
            output = check_output_inside_dir(
                "make help",
                str(result.project),
            )
            assert b"check code coverage quickly with the default Python" in output


@pytest.mark.parametrize(
    "license_info",
    [
        ("MIT license", "MIT "),
        (
            "BSD license",
            "Redistributions of source code must retain the above"
            " copyright notice, this",
        ),
        ("ISC license", "ISC License"),
        (
            "Apache Software License 2.0",
            "Licensed under the Apache License," " Version 2.0",
        ),
        ("GNU General Public License v3", "GNU GENERAL PUBLIC LICENSE"),
    ],
)
def test_bake_selecting_license(cookies, license_info):
    license, target_string = license_info
    with bake_in_temp_dir(
        cookies,
        extra_context={"open_source_license": license},
    ) as result:
        assert target_string in result.project.join("LICENSE").read()
        assert license in result.project.join("pyproject.toml").read()


def test_bake_not_open_source(cookies):
    with bake_in_temp_dir(
        cookies,
        extra_context={"open_source_license": "Not open source"},
    ) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert "pyproject.toml" in found_toplevel_files
        assert "LICENSE" not in found_toplevel_files
        assert "License" not in result.project.join("README.rst").read()


def test_bake_pre_commit(cookies):
    with bake_in_temp_dir(cookies) as result:
        found_toplevel_files = [f.basename for f in result.project.listdir()]
        assert ".pre-commit-config.yaml" in found_toplevel_files
        assert "pre-commit" in result.project.join("pyproject.toml").read()
