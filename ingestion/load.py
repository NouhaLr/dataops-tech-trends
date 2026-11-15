import duckdb
import pandas as pd

COLUMNS = ["objectID", "title", "url", "author", "points", "num_comments", "created_at_i"]


def load_raw(stories, db_path="warehouse.duckdb"):
    """Load stories into raw.hn_stories. Re-running never creates duplicates."""
    batch = pd.DataFrame(stories).reindex(columns=COLUMNS)

    con = duckdb.connect(db_path)
    con.execute("CREATE SCHEMA IF NOT EXISTS raw")
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS raw.hn_stories (
            story_id     VARCHAR PRIMARY KEY,
            title        VARCHAR,
            url          VARCHAR,
            author       VARCHAR,
            points       INTEGER,
            num_comments INTEGER,
            created_at   TIMESTAMP,
            _loaded_at   TIMESTAMP
        )
        """
    )
    con.register("batch", batch)
    con.execute(
        """
        INSERT OR REPLACE INTO raw.hn_stories
        SELECT
            objectID,
            title,
            url,
            author,
            points,
            num_comments,
            epoch_ms(CAST(created_at_i AS BIGINT) * 1000),
            current_timestamp
        FROM batch
        """
    )
    total = con.execute("SELECT count(*) FROM raw.hn_stories").fetchone()[0]
    con.close()
    return total