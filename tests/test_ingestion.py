import duckdb

from ingestion import hn
from ingestion.load import load_raw


def make_story(story_id, **overrides):
    """Build one fake HN story. Each test only gives the fields it wants to change."""
    story = {
        "objectID": story_id,
        "title": "Rust is fun",
        "url": "https://example.com",
        "author": "nouha",
        "points": 10,
        "num_comments": 2,
        "created_at_i": 1760000000,
    }
    return {**story, **overrides}


def test_loading_twice_creates_no_duplicates(tmp_path):
    db = str(tmp_path / "test.duckdb")
    stories = [make_story("1"), make_story("2")]
    load_raw(stories, db)
    total = load_raw(stories, db)
    assert total == 2


def test_reloading_updates_the_score_instead_of_duplicating(tmp_path):
    db = str(tmp_path / "test.duckdb")
    load_raw([make_story("1", points=10)], db)
    load_raw([make_story("1", points=99)], db)

    con = duckdb.connect(db, read_only=True)
    rows = con.execute("select story_id, points from raw.hn_stories").fetchall()
    con.close()
    assert rows == [("1", 99)]


def test_missing_field_does_not_crash(tmp_path):
    db = str(tmp_path / "test.duckdb")
    story = make_story("1")
    del story["url"]
    assert load_raw([story], db) == 1


class FakeResponse:
    def __init__(self, hits):
        self._hits = hits

    def raise_for_status(self):
        pass

    def json(self):
        return {"hits": self._hits}


class FakeSession:
    """Pretends to be the API: gives the pages one by one, then empty pages."""

    def __init__(self, pages):
        self.pages = pages
        self.calls = 0

    def get(self, *args, **kwargs):
        hits = self.pages[self.calls] if self.calls < len(self.pages) else []
        self.calls += 1
        return FakeResponse(hits)


def test_fetch_stops_on_empty_page(monkeypatch):
    session = FakeSession([[{"objectID": "1"}], [{"objectID": "2"}], []])
    monkeypatch.setattr(hn, "_build_session", lambda: session)

    stories = hn.fetch_stories(0, max_pages=5)

    assert len(stories) == 2
    assert session.calls == 3