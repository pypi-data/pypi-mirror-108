"""HTTP client configuration."""
import typing as t

from pydantic import AnyHttpUrl, BaseSettings
from requests import Request, auth

__all__ = ["AnyAuth", "HttpConfig"]

RETRY_METHODS = ["DELETE", "GET", "HEAD", "POST", "PUT", "OPTIONS"]
RETRY_STATUSES = [429, 500, 502, 503, 504]

AnyAuth = t.Union[
    str,  # authorization header (custom - the others are built in to requests)
    t.Tuple[str, str],  # basic auth user/pass
    t.Callable[[Request], Request],  # any callable modifying the request
    auth.AuthBase,  # same as above, implemented as a class
]


class HttpConfig(BaseSettings):
    """HTTP client configuration."""

    class Config:
        """Enable envvar config using prefix 'FW_HTTP_'."""

        env_prefix = "FW_HTTP_"

    client_name: str
    client_version: str
    client_info: t.Dict[str, str] = {}

    baseurl: t.Optional[AnyHttpUrl]
    cookies: t.Dict[str, str] = {}
    headers: t.Dict[str, str] = {}
    params: t.Dict[str, str] = {}
    cert: t.Optional[t.Union[str, t.Tuple[str, str]]]
    auth: t.Optional[AnyAuth]
    proxies: t.Dict[str, str] = {}
    verify: bool = True
    trust_env: bool = True
    connect_timeout: float = 5
    read_timeout: float = 15
    max_redirects: int = 30
    stream: bool = False
    response_hooks: t.List[t.Callable] = []
    retry_backoff_factor: float = 0.5
    retry_allowed_methods: t.List[str] = RETRY_METHODS
    retry_status_forcelist: t.List[int] = RETRY_STATUSES
    retry_total: int = 5
