import os
import threading
from enum import Enum
from functools import lru_cache
from importlib.util import find_spec
from typing import Literal, Protocol
from urllib import parse

from ._log import log


class SendFunction(Protocol):
    def __call__(self, url: str, params: dict[str, str | int], proxy: str | None, timeout: int) -> None:
        ...


class Lib(Enum):
    urllib = "urllib"
    requests = "requests"
    httpx = "httpx"
    requests_socks = "requests[socks]"
    httpx_socks = "httpx[socks]"


class LibChoised(Enum):
    urllib = "urllib"
    requests = "requests"
    httpx = "httpx"


class ProxyType(Enum):
    socks = "socks"
    http = "http"


@lru_cache(10)
def _parse_url(url: str) -> tuple[str, dict[str, str]]:
    parts = parse.urlsplit(url)

    base_url = parts.scheme + "://" + parts.netloc + parts.path
    params = dict(parse.parse_qsl(parts.query))

    return base_url, params


def _chek_available_libs() -> list[Lib]:
    available_libs = [Lib.urllib]

    if find_spec("requests"):
        available_libs.append(Lib.requests)
        if find_spec("socks"):
            available_libs.append(Lib.requests_socks)

    if find_spec("httpx"):
        available_libs.append(Lib.httpx)
        if find_spec("socksio"):
            available_libs.append(Lib.httpx_socks)

    return available_libs


def _choice_lib(proxy: str | None) -> LibChoised:
    if proxy and (not proxy.startswith("http") and not proxy.startswith("socks")):
            raise ValueError("Proxy must be starts with 'http' or 'socks'")

    proxy_type = None
    if proxy:
        proxy_type = ProxyType.socks if proxy.startswith("socks") else ProxyType.http

    available_libs = _chek_available_libs()

    select = LibChoised.urllib

    if proxy and proxy_type == ProxyType.socks:
        select = (
            LibChoised.httpx if Lib.httpx_socks in available_libs
            else LibChoised.requests if Lib.requests_socks in available_libs
            else None
        )

        if not select:
            raise ValueError("Socks proxy not supported install uk-send[httpx-socks] or uk-send[request-socks]")
        return select

    return (
        LibChoised.httpx if Lib.httpx in available_libs
        else LibChoised.requests if Lib.requests in available_libs
        else LibChoised.urllib
    )


@lru_cache(10)
def _get_send_function(proxy: str | None) -> SendFunction:
    lib = _choice_lib(proxy)

    if lib == LibChoised.httpx:
        from ._uk_send_httpx import send as send_httpx  # noqa: PLC0415
        log(f"send function: {"httpx"}")
        return send_httpx
    if lib == LibChoised.requests:
        from ._uk_send_requests import send as send_requests  # noqa: PLC0415
        log(f"send function: {"requests}"}")
        return send_requests

    from ._uk_send_urllib import send as send_urllib  # noqa: PLC0415
    log(f"send function: {"urllib"}")
    return send_urllib


def send(  # noqa: PLR0913
        msg: str = "",
        status: Literal["up", "down"] | None = None,
        ping: int | None = None,
        url: str | None = None,
        proxy: str | None = None,
        timeout: int = 5,
        thread: bool = True,
) -> None:

    url = url if url else os.getenv("UK_URL", None)
    if not url:
        return

    url, params_base = _parse_url(url)

    log(f"url {url}")
    log(f"params_base: {params_base}")

    proxy = proxy if proxy else os.getenv("UK_PROXY", None)

    log(f"proxy: {proxy}")

    send_function = _get_send_function(proxy)

    log(f"msg: {msg}, ping: {ping}, status: {status}")

    if not ping and ping != 0:
        if params_base.get("ping"):  # noqa: SIM108
            ping = int(params_base["ping"])
        else:
            ping = 1

    if not msg:
        if params_base.get("msg"):  # noqa: SIM108
            msg = params_base["msg"]
        else:
            msg = ""

    if not status:
        if params_base.get("status"):
            status = params_base["status"]  # pyright: ignore [reportAssignmentType]
            if status not in {"up", "down"}:
                status = "up"
        else:
            status = "up"

    log(f"msg: {msg}, ping: {ping}, status: {status}")

    params = {
        "status": status,
        "msg": msg,
        "ping": ping,
    }

    log(f"params: {params}")

    def send_() -> None:
        send_function(
            url=url,
            params=params,
            proxy=proxy,
            timeout=timeout,
        )

    if thread:
        t = threading.Thread(target=send_)
        t.start()
    else:
        send_()
