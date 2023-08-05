"""Prod-ready HTTP client with timeout and retries by default."""
import importlib.metadata

from .client import HttpClient, dump_useragent, load_useragent
from .config import AnyAuth, HttpConfig
from .errors import ClientError, ServerError

__all__ = [
    "AnyAuth",
    "ClientError",
    "ServerError",
    "HttpClient",
    "HttpConfig",
    "dump_useragent",
    "load_useragent",
]
__version__ = importlib.metadata.version(__name__)
