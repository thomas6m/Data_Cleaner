# Configuration Module Documentation

## Overview

Configuration module for data_cleaner package.

This module defines constants and settings used across the package for file handling, validation, logging, memory management, and lookup operations.

## Constants

### File Handling

- **`ALLOWED_EXTENSIONS`** (`list[str]`)  
  File extensions allowed for input files during conversion and validation.

- **`DEFAULT_CONVERT_DIR`** (`str`)  
  Default directory path to save converted CSV files.

- **`DEFAULT_OUTPUT_FORMAT`** (`str`)  
  Default output format for saved files; supports "csv" or "parquet".

- **`SUPPORTED_LOOKUP_EXTENSIONS`** (`tuple[str]`)  
  File extensions supported for lookup files: ".csv", ".parquet", ".json", ".jsonl", ".xls", ".xlsx".

### Processing Configuration

- **`DEFAULT_NUM_WORKERS`** (`int`)  
  Number of worker threads for parallel processing tasks.

- **`HEADER_VALIDATION_PATTERN`** (`str`)  
  Regex pattern to validate CSV header lines. Valid headers consist of comma-separated words that may include underscores or dashes.

### Logging Configuration

- **`DEFAULT_LOG_LEVEL`** (`int`)  
  Logging verbosity level (20 corresponds to INFO level).

- **`LOG_FORMAT`** (`str`)  
  Format string for log messages.

### Memory Management

- **`MAX_MEMORY_GB_DEFAULT`** (`float`)  
  Maximum recommended file size (in GB) for processing to avoid memory issues.

- **`CHUNK_SIZE_THRESHOLDS`** (`dict`)  
  Thresholds (in MB) to categorize file sizes for chunking strategy:
  - "small" < 50MB
  - "medium" 50MB to < 500MB  
  - "large" 500MB to < 2GB

- **`CHUNK_SIZE_VALUES`** (`dict`)  
  Number of rows to process per chunk, based on file size category:
  - small: 50,000 rows
  - medium: 100,000 rows
  - large: 200,000 rows
  - max_rows: 500,000 rows (hard limit)

- **`MEMORY_USAGE_FACTOR`** (`float`)  
  Factor estimating rows per MB of memory usage to adjust chunk sizes.

- **`ROWS_PER_MB`** (`int`)  
  Approximate number of rows per megabyte, used for memory calculations.

### Data Processing

- **`COLUMN_NAME_NORMALIZE_PATTERN`** (`re.Pattern`)  
  Regex pattern used to normalize column names by replacing non-word characters with underscores. Used in lookup-related operations.

## Usage

Import this module to access configuration constants needed for file processing, validation, logging setup, and lookup table operations within the data_cleaner package.

```python
from data_cleaner import config

# Access configuration constants
allowed_exts = config.ALLOWED_EXTENSIONS
chunk_size = config.CHUNK_SIZE_VALUES['medium']
log_level = config.DEFAULT_LOG_LEVEL
```