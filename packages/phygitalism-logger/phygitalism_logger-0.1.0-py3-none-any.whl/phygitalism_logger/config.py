import os

from phygitalism_config.config import Config


class Logging(Config):
    is_graylog: bool = False
    debug: bool = False
    is_debug_log: bool = False
    simple_formatter: str = "[%(levelname)s:%(name)s] [%(asctime)s] %(lineno)d %(message)s"
    extended_formatter: str = "[%(levelname)s:%(name)s] [%(asctime)s] %(lineno)d |"\
                              " %(module)s - %(filename)s - %(funcName)s | %(message)s"
    level: str = 'INFO'


class GraylogFile(Config):
    path: str


class Graylog(Config):
    if GraylogFile.path:
        _load_from = GraylogFile.path

    host: str
    port: int
    level: str = 'INFO'
    project_name: str = 'none'
    project_version: str = 'none'
    debug: bool


class DebugLogFile(Config):
    path: str


class DebugLog(Config):
    if DebugLogFile.path:
        _load_from = DebugLogFile.path
    file_path: str
    max_bytes: int
    backup_count: int
