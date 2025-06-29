# data_cleaner/utils.py
import re
import os
import polars as pl
from typing import List, Optional
from data_cleaner.config import (
    HEADER_VALIDATION_PATTERN,
    ALLOWED_EXTENSIONS,
    CHUNK_SIZE_THRESHOLDS,
    CHUNK_SIZE_VALUES,
    MEMORY_USAGE_FACTOR,
    ROWS_PER_MB,
)

def validate_header_line(header: str) -> bool:
    if not header or not header.strip():
        return False
    return bool(re.match(HEADER_VALIDATION_PATTERN, header.strip(), flags=re.UNICODE))

def validate_file_path(file_path: str, allowed_extensions: List[str] = None) -> bool:
    if allowed_extensions is None:
        allowed_extensions = ALLOWED_EXTENSIONS
    # ... rest remains the same

def calculate_optimal_chunk_size(file_size_mb: float, available_memory_mb: float) -> int:
    if file_size_mb < CHUNK_SIZE_THRESHOLDS["small"]:
        return CHUNK_SIZE_VALUES["small"]
    elif file_size_mb < CHUNK_SIZE_THRESHOLDS["medium"]:
        return CHUNK_SIZE_VALUES["medium"]
    elif file_size_mb < CHUNK_SIZE_THRESHOLDS["large"]:
        return CHUNK_SIZE_VALUES["large"]
    else:
        memory_based_rows = int(available_memory_mb * MEMORY_USAGE_FACTOR * ROWS_PER_MB)
        return min(max(memory_based_rows, CHUNK_SIZE_VALUES["medium"]), CHUNK_SIZE_VALUES["max_rows"])
