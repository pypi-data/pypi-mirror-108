# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_framework', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter', 'dynaconf', 'fire', 'loguru', 'termcolor', 'toml']

entry_points = \
{'console_scripts': ['shanx-py = python_framework.main:main']}

setup_kwargs = {
    'name': 'shanx-framework',
    'version': '0.1.6',
    'description': 'Python Framework',
    'long_description': "================\nPython Framework\n================\n\n.. image:: https://github.com/sp-95/python-framework/workflows/Tests/badge.svg\n    :target: https://github.com/sp-95/python-framework/actions?query=workflow%3ATests\n    :alt: Tests\n\n.. image:: https://github.com/sp-95/python-framework/workflows/Documentation/badge.svg\n    :target: https://sp-95.github.io/python-framework/\n    :alt: Documentation\n\n.. image:: https://github.com/sp-95/python-framework/workflows/Release/badge.svg\n    :target: https://pypi.python.org/pypi/python-framework\n    :alt: Release\n\n.. image:: https://img.shields.io/pypi/v/shanx-framework.svg\n    :target: https://pypi.python.org/pypi/shanx-framework\n    :alt: PyPi Version\n\nCookiecutter_ template for Python Framework.\n\n* **Source Code**: https://github.com/sp-95/python-framework\n* **Documentation**: https://sp-95.github.io/python-framework/\n* **Bug Reports**: https://github.com/sp-95/python-framework/issues\n\nFeatures\n--------\n\n* poetry_: Dependency Management\n* `Editor Config`_: Maintains Code Consistency\n* flake8_: Linting\n* black_ and isort_: Code Formatting\n* mypy_: Type Hinting\n* pre_commit_hooks_: Git hooks\n* fire_: Command-line Interface\n* loguru_: Logging\n* dynaconf_: Configuration Management\n* pytest_ and coverage_: Python Testing and Code Coverage\n* Tox_: Automated and Standardized testing\n* Sphinx_: Generates documents automatically\n* `GitHub Actions`_: Continuous Integration\n* `GitHub Pages`_: Documentation Hosting\n* PyPi_: Auto-deploy when you make a release (optional)\n* GitHub issue templates\n\nQuickstart\n----------\n\n#. Install the latest framework for Python if you haven't installed it yet\n\n   .. code-block:: console\n\n        $ pip install -U python-framework\n\n#. Initialize your project\n\n   .. code-block:: console\n\n        $ shanx-py init\n\n#. Create a repo and put it there.\n#. Generate the docs by pushing your first commit to master.\n#. Deploy your package to PyPi_ by pushing a tag and creating a release.\n\nFor more details, see the `python-framework tutorial`_.\n\nAcknowledgment\n---------------\n\nThis package is a modified duplicate of the `audreyr/cookiecutter-pypackage`_\nproject template\n\n.. _Cookiecutter: https://github.com/cookiecutter/cookiecutter\n.. _poetry: https://python-poetry.org/docs/\n.. _Editor Config: https://editorconfig.org/\n.. _flake8: https://pypi.org/project/flake8/\n.. _black: https://black.readthedocs.io/en/stable/\n.. _isort: https://pycqa.github.io/isort/\n.. _mypy: http://mypy-lang.org/\n.. _pre_commit_hooks: https://github.com/pre-commit/pre-commit-hooks\n.. _fire: https://google.github.io/python-fire/guide/\n.. _loguru: https://loguru.readthedocs.io/en/stable/\n.. _dynaconf: https://www.dynaconf.com/\n.. _pytest: https://docs.pytest.org/en/stable/\n.. _coverage: https://coverage.readthedocs.io/en/coverage-5.3/\n.. _Tox: http://testrun.org/tox/\n.. _Sphinx: http://sphinx-doc.org/\n.. _GitHub Actions: https://docs.github.com/en/free-pro-team@latest/actions\n.. _GitHub Pages: https://docs.github.com/en/free-pro-team@latest/github/working-with-github-pages\n.. _PyPi: https://pypi.python.org/pypi\n.. _python-framework tutorial: https://sp-95.github.io/python-framework/tutorial.html\n.. _audreyr/cookiecutter-pypackage: https://github.com/audreyfeldroy/cookiecutter-pypackage\n",
    'author': 'Shashanka Prajapati',
    'author_email': 'shashankap95@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sp-95/python-framework',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
