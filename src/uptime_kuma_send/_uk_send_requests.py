import requests


def send(url: str, params: dict[str, str | int], proxy: str | None, timeout: int) -> None:
    requests.get(
        url,
        params=params,
        timeout=timeout,
        proxies={
            "http": proxy,
            "https": proxy,
        } if proxy else None,
    )