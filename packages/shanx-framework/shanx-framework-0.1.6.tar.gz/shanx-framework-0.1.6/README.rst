================
Python Framework
================

.. image:: https://github.com/sp-95/python-framework/workflows/Tests/badge.svg
    :target: https://github.com/sp-95/python-framework/actions?query=workflow%3ATests
    :alt: Tests

.. image:: https://github.com/sp-95/python-framework/workflows/Documentation/badge.svg
    :target: https://sp-95.github.io/python-framework/
    :alt: Documentation

.. image:: https://github.com/sp-95/python-framework/workflows/Release/badge.svg
    :target: https://pypi.python.org/pypi/python-framework
    :alt: Release

.. image:: https://img.shields.io/pypi/v/shanx-framework.svg
    :target: https://pypi.python.org/pypi/shanx-framework
    :alt: PyPi Version

Cookiecutter_ template for Python Framework.

* **Source Code**: https://github.com/sp-95/python-framework
* **Documentation**: https://sp-95.github.io/python-framework/
* **Bug Reports**: https://github.com/sp-95/python-framework/issues

Features
--------

* poetry_: Dependency Management
* `Editor Config`_: Maintains Code Consistency
* flake8_: Linting
* black_ and isort_: Code Formatting
* mypy_: Type Hinting
* pre_commit_hooks_: Git hooks
* fire_: Command-line Interface
* loguru_: Logging
* dynaconf_: Configuration Management
* pytest_ and coverage_: Python Testing and Code Coverage
* Tox_: Automated and Standardized testing
* Sphinx_: Generates documents automatically
* `GitHub Actions`_: Continuous Integration
* `GitHub Pages`_: Documentation Hosting
* PyPi_: Auto-deploy when you make a release (optional)
* GitHub issue templates

Quickstart
----------

#. Install the latest framework for Python if you haven't installed it yet

   .. code-block:: console

        $ pip install -U python-framework

#. Initialize your project

   .. code-block:: console

        $ shanx-py init

#. Create a repo and put it there.
#. Generate the docs by pushing your first commit to master.
#. Deploy your package to PyPi_ by pushing a tag and creating a release.

For more details, see the `python-framework tutorial`_.

Acknowledgment
---------------

This package is a modified duplicate of the `audreyr/cookiecutter-pypackage`_
project template

.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter
.. _poetry: https://python-poetry.org/docs/
.. _Editor Config: https://editorconfig.org/
.. _flake8: https://pypi.org/project/flake8/
.. _black: https://black.readthedocs.io/en/stable/
.. _isort: https://pycqa.github.io/isort/
.. _mypy: http://mypy-lang.org/
.. _pre_commit_hooks: https://github.com/pre-commit/pre-commit-hooks
.. _fire: https://google.github.io/python-fire/guide/
.. _loguru: https://loguru.readthedocs.io/en/stable/
.. _dynaconf: https://www.dynaconf.com/
.. _pytest: https://docs.pytest.org/en/stable/
.. _coverage: https://coverage.readthedocs.io/en/coverage-5.3/
.. _Tox: http://testrun.org/tox/
.. _Sphinx: http://sphinx-doc.org/
.. _GitHub Actions: https://docs.github.com/en/free-pro-team@latest/actions
.. _GitHub Pages: https://docs.github.com/en/free-pro-team@latest/github/working-with-github-pages
.. _PyPi: https://pypi.python.org/pypi
.. _python-framework tutorial: https://sp-95.github.io/python-framework/tutorial.html
.. _audreyr/cookiecutter-pypackage: https://github.com/audreyfeldroy/cookiecutter-pypackage
