# lookup.py - Lookup Table Integration Module for data_cleaner

This module enables enrichment of datasets by performing left joins with external lookup tables (CSV, Excel, JSON, etc.) using Polars for high-performance processing.

## Core Features

- Normalizes column names for robust joins (lowercase, underscore-delimited)
- Caches lookup tables in-memory for faster repeated usage
- Supports various file formats (CSV, Parquet, Excel, JSON, JSONL)
- Logs each major step with performance metrics

## Functions

### `normalize_column_name(col: str) -> str`
Normalizes column names to a consistent format.

### `get_lookup_df(lookup_path: str, use_cache: bool = True) -> pl.DataFrame`
Loads a lookup table from disk and caches it for repeated use.

### `apply_lookup(main_df: pl.DataFrame, lookup_path: str, lookup_key: str, return_columns: List[str], use_cache: bool = True) -> pl.DataFrame`
Joins main data with a lookup table to enrich fields using a left join.

## Example Usage

```python
from data_cleaner.lookup import apply_lookup

df_enriched = apply_lookup(
    main_df=pl.read_csv("input.csv"),
    lookup_path="lookup.csv",
    lookup_key="email",
    return_columns=["region", "user_type"]
)
```

## Supported Formats

- `.csv`
- `.parquet`
- `.json` / `.jsonl`
- `.xls` / `.xlsx` (via pandas)

## Configuration

- `COLUMN_NAME_NORMALIZE_PATTERN` from config.py
- `SUPPORTED_LOOKUP_EXTENSIONS` from config.py

## Logging

- Uses the global logger setup in logger_setup.py
- Each major step (load, normalize, join) is timed and logged via log_step

## Cache

Global cache for performance boost if `use_cache=True`

## Exceptions Raised

- `FileNotFoundError`
- `RuntimeError` (read/load failure)
- `ValueError` (join key or return fields missing)