# Tech Trends: a DataOps pipeline

Collects Hacker News stories every day, checks their quality, and publishes trusted indicators.

## Pipeline

Hacker News API -> Python ingestion -> DuckDB (raw) -> dbt (staging -> quality rules -> marts) -> tests

## Run it (Windows PowerShell)

    py -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python run_ingestion.py
    dbt build
    python -m pytest

## Business questions

1. Which keywords are rising compared with last week?
2. Does a topic exploding on Hacker News raise Wikipedia pageviews the next day?
3. Is today's data fresh, complete and free of duplicates?

## Status

- Done: ingestion without duplicates, dbt layers, data tests, unit tests
- Next: Wikipedia source, data contract, CI, Prefect, Docker, data health page, alert