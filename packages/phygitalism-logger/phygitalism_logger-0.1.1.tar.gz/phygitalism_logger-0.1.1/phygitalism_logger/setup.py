import os
import logging
import logging.config
from typing import Optional

from .config import *

environment = os.environ.get('ENVIRONMENT', 'local')

graylog_gelf_config = {
    "class": "pygelf.GelfUdpHandler",
    "level": logging.getLevelName(Graylog.level.upper()),
    "host": Graylog.host,
    "port": Graylog.port,
    "debug": Graylog.debug,
    "include_extra_fields": True,
    "project_name": Graylog.project_name,
    "project_version": Graylog.project_version,
    "build_name": environment
}

debug_file_config = {
    "class": "logging.handlers.RotatingFileHandler",
    "level": logging.DEBUG,
    "formatter": "extended",
    "filename": DebugLog.file_path,
    "maxBytes": DebugLog.max_bytes,
    "backupCount": DebugLog.backup_count,
    "encoding": "utf8",
    "delay": True
}

logger_config = {
    "level": logging.getLevelName(Logging.level.upper()),
    "propogate": True,
    "handlers": [
        "console",
    ]
}

handlers = []

default_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": Logging.simple_formatter
        },
        "extended": {
            "format": Logging.extended_formatter
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": logging.getLevelName(Logging.level.upper()),
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        },
    },
    "loggers": {},
    "root": {
        "level": logging.getLevelName(Logging.level.upper()),
        "handlers": handlers
    }
}


def setup(project_name: Optional[str] = None, dict_config: Optional[dict] = None):
    if Logging.is_graylog and environment != 'local':
        handlers.append('graylog_gelf')
        default_config['handlers']['graylog_gelf'] = graylog_gelf_config
        project_name = Graylog.project_name
    if Logging.is_debug_log:
        handlers.append('file_handler')
        default_config['handlers']['file_handler'] = debug_file_config

    if not project_name:
        project_name = __name__.split('.')[0]

    default_config['loggers'][project_name] = logger_config
    default_config['loggers'][f"{project_name}.*"] = logger_config

    if dict_config:
        default_config.update(dict_config)

    logging.config.dictConfig(default_config)
