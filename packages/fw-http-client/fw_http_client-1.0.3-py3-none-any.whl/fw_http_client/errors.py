"""HTTP client errors."""
import re
import typing as t

# pylint: disable=wildcard-import,unused-wildcard-import,redefined-builtin
from requests.exceptions import *

__all__ = ["ClientError", "ServerError"]


class ClientError(HTTPError):
    """The server returned a response with 4xx status."""


class ServerError(HTTPError):
    """The server returned a response with 5xx status."""


def request_exception_getattr(self, name: str):
    """Proxy the response and the request attributes for convenience."""
    try:
        return getattr(self.response, name)
    except AttributeError:
        pass
    try:
        return getattr(self.request, name)
    except AttributeError:
        pass
    raise AttributeError(f"{type(self).__name__} has no attribute {name!r}")


def request_exception_str(self) -> str:
    """Return the string representation of a RequestException."""
    return f"{self.method} {self.url} - {self.args[0]}"  # pragma: no cover


def connection_error_str(self) -> str:
    """Return the string representation of a ConnectionError."""
    msg = str(self.args[0])
    if "Errno" in msg:
        msg = re.sub(r".*(\[[^']*).*", r"\1", msg)
    if "read timeout" in msg:
        msg = re.sub(r'.*: ([^"]*).*', r"\1", msg)
    return f"{self.method} {self.url} - {msg}"


def http_error_str(self) -> str:
    """Return the string representation of an HTTPError."""
    msg = f"{self.method} {self.url} - {self.status_code} {self.reason}"
    # capture the request body we sent
    if request_body := truncate(self.body):
        join = "\n" if "\n" in request_body else " "
        msg += f"\nRequest:{join}{request_body}"
    # add anything the server had to say about the problem
    if response_content := truncate(self.content):
        join = "\n" if "\n" in response_content else " "
        msg += f"\nResponse:{join}{response_content}"
    return msg


def truncate(data: t.Optional[bytes], max_length: int = 256) -> str:
    """Return bytes truncated to the specified length as a string."""
    if not data:
        return ""
    data = data.rstrip()
    if len(data) > max_length:
        data = data[: max_length - 3].rstrip() + b"..."
    try:
        return data.decode()
    except UnicodeDecodeError:  # pragma: no cover
        return str(data)


# patch the exceptions for more useful default error messages
RequestException.__getattr__ = request_exception_getattr  # type: ignore
RequestException.__str__ = request_exception_str  # type: ignore
ConnectionError.__str__ = connection_error_str  # type: ignore
HTTPError.__str__ = http_error_str  # type: ignore
