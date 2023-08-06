import inspect
import logging
import os
import sys
from types import TracebackType
from typing import *

from .setup import setup

_base = os.path.abspath('.')


class ProxyLogger(logging.Logger):
    def __init__(self):
        super().__init__(__name__)

    def makeRecord(
            self,
            name: str,
            level: int,
            fn: str,
            lno: int,
            msg: Any,
            args: Union[Tuple[Any, ...], Mapping[str, Any]],
            exc_info: Optional[
                Union[Tuple[type, BaseException, Optional[TracebackType]], Tuple[None, None, None], None]],
            func: Optional[str] = None,
            extra: Optional[Mapping[str, Any]] = None,
            sinfo: Optional[str] = None,
    ) -> logging.LogRecord:
        base = os.path.basename(fn)
        if base == '<input>':
            name = '__main__'
        else:
            for p in sys.path:
                if fn.startswith(p):
                    path = fn.replace(p, '')
                    path = path.replace('__init__.py', '')
                    path = path.replace('.py', '')
                    name = '.'.join(path.split('/'))
                    name = name.strip('.')
        return super(ProxyLogger, self).makeRecord(
            name,
            level,
            fn,
            lno,
            msg,
            args,
            exc_info,
            func,
            extra,
            sinfo
        )


logger = ProxyLogger()

__all__ = (
    logger,
    setup
)
