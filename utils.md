# utils.py - Utility Functions for data_cleaner

This module provides reusable utility functions used across the data cleaning pipeline, including file validation, header checking, and memory-based chunk size estimation.

## Functions

### 1. validate_header_line(header: str) -> bool

Validates a CSV header line using a regex pattern.

- Returns True if the header is non-empty and matches the defined pattern.
- Pattern allows comma-separated words, with optional dashes or underscores.

### 2. validate_file_path(file_path: str, allowed_extensions: List[str] = None) -> bool

Validates that:
- The file path exists and is accessible
- The file has an allowed extension
- Prevents insecure paths (e.g., containing '..')
- Uses ALLOWED_EXTENSIONS from config if not provided.

### 3. calculate_optimal_chunk_size(file_size_mb: float, available_memory_mb: float) -> int

Determines the number of rows to process in a chunk based on:
- File size (MB)
- Available system memory (MB)
- Heuristics from CHUNK_SIZE_THRESHOLDS, CHUNK_SIZE_VALUES, MEMORY_USAGE_FACTOR

**Returns:**
- Optimal row count for the next chunk to load based on file/memory profile.

## Constants Imported from config.py

- **HEADER_VALIDATION_PATTERN**: Regex to validate header row structure
- **ALLOWED_EXTENSIONS**: Permitted input file types
- **CHUNK_SIZE_THRESHOLDS**: File size cutoffs (small, medium, large)
- **CHUNK_SIZE_VALUES**: Corresponding row chunk sizes for thresholds
- **MEMORY_USAGE_FACTOR**: Ratio to control memory-based chunking
- **ROWS_PER_MB**: Heuristic estimate of row count per MB

## Usage Example

```python
from data_cleaner.utils import validate_header_line, calculate_optimal_chunk_size

if validate_header_line("name,email,age"):
    print("Valid header!")
    
rows_to_read = calculate_optimal_chunk_size(file_size_mb=100, available_memory_mb=2048)
```

## Dependencies

- re
- os
- polars (imported but not currently used here)
- typing