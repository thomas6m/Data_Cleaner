# data_cleaner/lookup.py
import polars as pl
import os
import re
from typing import List, Optional

from data_cleaner.logger_setup import setup_logging
from data_cleaner.perf_utils import log_step
from data_cleaner.config import COLUMN_NAME_NORMALIZE_PATTERN, SUPPORTED_LOOKUP_EXTENSIONS

logger = setup_logging()

# Global cache for lookup DataFrame
_cached_lookup_df: Optional[pl.DataFrame] = None
_cached_lookup_path: Optional[str] = None

def normalize_column_name(col: str) -> str:
    """
    Normalize column name by stripping, lowering, and replacing non-word chars with underscores.
    """
    return COLUMN_NAME_NORMALIZE_PATTERN.sub('_', col.strip().lower())

def get_lookup_df(lookup_path: str, use_cache: bool = True) -> pl.DataFrame:
    """
    Load and cache lookup DataFrame from file.

    Args:
        lookup_path: Path to the lookup file.
        use_cache: Whether to use cached DataFrame if available.

    Returns:
        polars.DataFrame: Loaded lookup data.
    
    Raises:
        FileNotFoundError: If lookup file does not exist.
        RuntimeError: If reading the lookup file fails.
        ValueError: For unsupported file types.
    """
    global _cached_lookup_df, _cached_lookup_path

    if use_cache and _cached_lookup_df is not None and _cached_lookup_path == lookup_path:
        logger.info("🔁 Using cached lookup DataFrame.")
        return _cached_lookup_df

    with log_step("Load lookup file"):
        if not os.path.isfile(lookup_path):
            logger.error(f"Lookup file not found: {lookup_path}")
            raise FileNotFoundError(f"Lookup file not found: {lookup_path}")

        ext = lookup_path.lower()
        if not ext.endswith(SUPPORTED_LOOKUP_EXTENSIONS):
            raise ValueError(f"Unsupported lookup file type: {lookup_path}")

        try:
            if ext.endswith(".csv"):
                df = pl.read_csv(lookup_path)
            elif ext.endswith(".parquet"):
                df = pl.read_parquet(lookup_path)
            elif ext.endswith(".json"):
                df = pl.read_json(lookup_path)
            elif ext.endswith(".jsonl"):
                df = pl.read_ndjson(lookup_path)
            elif ext.endswith((".xls", ".xlsx")):
                import pandas as pd
                df = pl.from_pandas(pd.read_excel(lookup_path))
        except Exception as e:
            logger.error(f"Failed to load lookup file: {e}")
            raise RuntimeError(f"Failed to load lookup file: {e}")

        if use_cache:
            _cached_lookup_df = df
            _cached_lookup_path = lookup_path
            logger.info(f"✅ Cached lookup DataFrame from: {lookup_path}")
        else:
            logger.info(f"📤 Lookup loaded without caching: {lookup_path}")

        return df

def apply_lookup(
    main_df: pl.DataFrame,
    lookup_path: str,
    lookup_key: str,
    return_columns: List[str],
    use_cache: bool = True,
) -> pl.DataFrame:
    """
    Enrich main DataFrame by joining with lookup DataFrame on the lookup key.

    Args:
        main_df: Main polars DataFrame to enrich.
        lookup_path: File path to lookup table.
        lookup_key: Column name to join on.
        return_columns: List of columns to fetch from lookup table.
        use_cache: Whether to cache the lookup DataFrame.

    Returns:
        polars.DataFrame: Enriched DataFrame after join.

    Raises:
        ValueError: If join key or return columns are missing.
    """
    lookup_df = get_lookup_df(lookup_path, use_cache=use_cache)

    with log_step("Normalize and join lookup"):
        # Normalize column names
        lookup_df = lookup_df.rename({col: normalize_column_name(col) for col in lookup_df.columns})
        main_df = main_df.rename({col: normalize_column_name(col) for col in main_df.columns})

        lookup_key_norm = normalize_column_name(lookup_key)
        return_columns_norm = [normalize_column_name(col) for col in return_columns]

        # Validate presence of join key
        if lookup_key_norm not in main_df.columns:
            logger.error(f"Join key '{lookup_key_norm}' missing from main data columns: {main_df.columns}")
            raise ValueError(f"Join key '{lookup_key_norm}' must be in main DataFrame columns.")
        if lookup_key_norm not in lookup_df.columns:
            logger.error(f"Join key '{lookup_key_norm}' missing from lookup data columns: {lookup_df.columns}")
            raise ValueError(f"Join key '{lookup_key_norm}' must be in lookup DataFrame columns.")

        # Validate presence of return columns
        missing = [col for col in return_columns_norm if col not in lookup_df.columns]
        if missing:
            logger.error(f"Missing lookup fields: {missing} in lookup file columns: {lookup_df.columns}")
            raise ValueError(f"Missing lookup fields in file: {missing}")

        # Select relevant columns from lookup DataFrame
        selected_cols = [lookup_key_norm] + return_columns_norm
        lookup_df = lookup_df.select(selected_cols)

        # Perform left join
        enriched_df = main_df.join(lookup_df, on=lookup_key_norm, how="left")
        logger.info(f"🔗 Lookup join completed on key: {lookup_key_norm}")

    return enriched_df
