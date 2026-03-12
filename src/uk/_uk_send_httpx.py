import httpx


def send(url: str, params: dict[str, str | int], proxy: str | None, timeout: int) -> None:
    httpx.get(
        url,
        params=params,
        timeout=timeout,
        proxy=proxy if proxy else None,
    )