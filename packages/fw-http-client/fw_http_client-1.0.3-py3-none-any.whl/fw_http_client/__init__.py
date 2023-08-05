"""Prod-ready HTTP client with timeout and retries by default."""
import importlib.metadata

from . import errors
from .client import HttpClient, dump_useragent, load_useragent
from .config import AnyAuth, HttpConfig
from .errors import ConnectionError  # pylint: disable=redefined-builtin
from .errors import ClientError, ServerError

__version__ = importlib.metadata.version(__name__)
__all__ = [
    "AnyAuth",
    "HttpClient",
    "HttpConfig",
    "dump_useragent",
    "load_useragent",
    "errors",
    "ConnectionError",
    "ClientError",
    "ServerError",
]
