import requests


def get_oidc_config(url: str, timeout: int = 10):
    response = requests.get(
        url,
        allow_redirects=True,
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()
