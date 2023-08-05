import os
import subprocess
from distutils import spawn

import fire
import toml
from cookiecutter import exceptions
from cookiecutter.main import cookiecutter
from loguru import logger


class Main:
    @property
    def version(self):
        try:
            return self._version
        except AttributeError:
            self._version = self._get_project_meta()["version"]
            return self._version

    @staticmethod
    def _get_project_meta():
        return toml.load("pyproject.toml")["tool"]["poetry"]

    @staticmethod
    def init():
        if not spawn.find_executable("git"):
            logger.warning("git not installed in your system")
            logger.info("Downloading git")
            subprocess.run(["sudo", "apt", "install", "git"])

        if not spawn.find_executable("python3"):
            logger.warning("python3 not installed in your system")
            logger.info("Downloading python3")
            subprocess.run(["sudo", "apt", "install", "python3"])

        if not spawn.find_executable("poetry"):
            logger.warning("poetry not installed")
            logger.info("Installing poetry")
            subprocess.run(
                ["pip3", "install", "poetry", "--user", "--upgrade", "--pre"],
            )

        while True:
            try:
                path = cookiecutter("gh:sp-95/python-framework")
                os.chdir(path)
                subprocess.run(["git", "init"])
                subprocess.run(["poetry", "install"])
                subprocess.run(["poetry", "run", "pre-commit", "install"])
                break
            except exceptions.RepositoryNotFound:
                logger.error("Download incomplete!")
            except exceptions.FailedHookException:
                logger.error("Please enter valid inputs")
            except exceptions.OutputDirExistsException as e:
                logger.error(str(e))
                break


def main():
    fire.Fire(Main)
