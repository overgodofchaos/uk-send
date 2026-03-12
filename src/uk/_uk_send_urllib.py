import urllib.parse
import urllib.request


def send(url: str, params: dict[str, str | int], proxy: str | None, timeout: int) -> None:
    if proxy and not proxy.startswith("http"):
        raise ValueError("Urllib supports only http proxy.")

    if proxy:
        proxy_handler = urllib.request.ProxyHandler({
            "http": proxy,
            "https": proxy,
        })
        opener = urllib.request.build_opener(proxy_handler)
    else:
        opener = urllib.request.build_opener()

    params_str = urllib.parse.urlencode(params)

    opener.open(f"{url}?{params_str}", timeout=timeout)