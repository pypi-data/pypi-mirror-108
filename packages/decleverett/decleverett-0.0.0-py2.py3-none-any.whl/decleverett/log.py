# -*- coding: utf-8 -*-
import logging.config
from functools import lru_cache
from typing import Union

from decleverett.base import Config, Core, Param


def _get_log_level(level_name: Union[str, int], default=logging.DEBUG):
    if isinstance(level_name, str):
        level_name = logging._nameToLevel.get(
            level_name, default
        )  # pylint: disable=protected-access
    return level_name


@lru_cache
def get_logger(
    logger_name, log_namespace='', default_level: Union[str, int] = logging.INFO
):
    class Logging(Config):
        """Logging config"""

        namespace = log_namespace
        LOG_LEVEL = Param(
            default='INFO' if not Core.DEBUG else 'DEBUG',
            doc='Logging level',
            parser=str,
        )

    level = _get_log_level(Logging.LOG_LEVEL, default_level)

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'}
        },
        'handlers': {
            'default': {
                'level': level,
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            }
        },
        'loggers': {
            logger_name: {
                'handlers': ['default'],
                'level': level,
            }
        },
    }

    logging.config.dictConfig(logging_config)

    return logging.getLogger(logger_name)
