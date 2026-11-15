import time

from ingestion.hn import fetch_stories
from ingestion.load import load_raw


def main(hours=24):
    since_ts = int(time.time()) - hours * 3600
    print(f"[1/2] Fetching stories from the last {hours}h")
    stories = fetch_stories(since_ts)
    print(f"      {len(stories)} stories fetched")

    print("[2/2] Loading into DuckDB")
    total = load_raw(stories)
    print(f"      raw.hn_stories now holds {total} rows")


if __name__ == "__main__":
    main()