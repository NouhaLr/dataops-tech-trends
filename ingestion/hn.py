import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://hn.algolia.com/api/v1/search_by_date"


def _build_session():
    """A session that retries on network errors and on temporary server errors."""
    retry = Retry(
        total=4,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def fetch_stories(since_ts, max_pages=5):
    """Fetch HN stories created after `since_ts` (unix seconds)."""
    session = _build_session()
    stories = []
    for page in range(max_pages):
        response = session.get(
            BASE_URL,
            params={
                "tags": "story",
                "hitsPerPage": 50,
                "page": page,
                "numericFilters": f"created_at_i>{since_ts}",
            },
            timeout=(10, 60),
        )
        response.raise_for_status()
        hits = response.json()["hits"]
        if not hits:
            break
        stories.extend(hits)
    return stories