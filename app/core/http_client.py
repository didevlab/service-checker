import httpx


def create_http_client(
    timeout_seconds: float,
    user_agent: str,
) -> httpx.AsyncClient:
    headers = {"User-Agent": user_agent}
    return httpx.AsyncClient(timeout=timeout_seconds, headers=headers)

