import logging
import sys
from typing import Union

from loguru import logger
from loguru._defaults import LOGURU_FORMAT

from python_framework.config import settings


class InterceptHandler(logging.Handler):  # pragma: no cover
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists
        try:
            level: Union[int, str] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            if frame.f_back:
                frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


class LogConfig:
    FORMAT = settings.get("log_format", LOGURU_FORMAT)

    @staticmethod
    def setup() -> None:
        level = "DEBUG" if settings.debug else "INFO"

        # intercept everything at the root logger
        logging.root.handlers = [InterceptHandler()]
        logging.root.setLevel(level)

        # remove every other logger's handlers
        # and propagate to root logger
        for name in logging.root.manager.loggerDict.keys():  # type: ignore
            logging.getLogger(name).handlers = []
            logging.getLogger(name).propagate = True

        logger.configure(
            handlers=[{"sink": sys.stdout, "level": level, "format": LogConfig.FORMAT}],
        )

        for level in ["critical", "error", "warning", "info", "debug"]:
            logger.add(
                settings.LOG_PATH / f"{level}.log",
                level=level.upper(),
                format=LogConfig.FORMAT,
                rotation="10MB",
            )


log_config = LogConfig()
