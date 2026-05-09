import requests
from config import API_BASE_URL


def fetch_player(tag: str, token: str) -> dict:
    # tag arrives without '#'; URL already encodes it as %23
    url = API_BASE_URL.format(tag=tag.lstrip("#"))
    resp = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(
            f"CR API returned {resp.status_code} for tag '{tag}': {resp.text}"
        )
    return resp.json()
