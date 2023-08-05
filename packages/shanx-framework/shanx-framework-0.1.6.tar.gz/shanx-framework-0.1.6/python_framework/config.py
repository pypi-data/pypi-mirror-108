from pathlib import Path
from typing import Any

import toml
from dynaconf import Dynaconf

_BASE_PATH = Path(__file__).parent.parent
_CONFIG_PATH = _BASE_PATH / "configs"


class Config(Dynaconf):
    def __init__(self, **kwargs: Any) -> None:
        super(Config, self).__init__(**kwargs)
        self.env = self.env_for_dynaconf.lower()

        if not hasattr(self, "debug"):
            self.debug = True if self.env not in ["prod", "production"] else False

        self.base_path = _BASE_PATH

        self.config_path = _CONFIG_PATH
        self.log_path = self.base_path / "logs"

        self.project_meta = toml.load(self.base_path / "pyproject.toml")["tool"][
            "poetry"
        ]


settings = Config(
    envvar_prefix="SHANX",
    settings_files=[
        _CONFIG_PATH / "settings.yaml",
        _CONFIG_PATH / ".secrets.yaml",
    ],
    environments=True,
)

# `envvar_prefix` = export envvars with `export SHANX_FOO=bar`.
# `settings_files` = Load this files in the order.
# `environments` = Set Project environment with `export ENV_FOR_DYNACONF=development`
