# data_cleaner/config.py

import os
import re

# Allowed input file extensions for conversion & validation
ALLOWED_EXTENSIONS = [
    ".csv",
    ".parquet",
    ".xls",
    ".xlsx",
    ".txt",
    ".tsv",
    ".json",
    ".jsonl",
]

# Default directory to save converted CSV files
DEFAULT_CONVERT_DIR = os.path.join(os.getcwd(), "converted")

# Default number of worker threads for parallel processing
DEFAULT_NUM_WORKERS = 4

# Default output file format
DEFAULT_OUTPUT_FORMAT = "csv"  # Options: "csv" or "parquet"

# Header validation regex pattern: 
# Valid header line contains comma-separated words with optional underscores/dashes
HEADER_VALIDATION_PATTERN = r"^([\w\-]+)(,[\w\-]+)*$"

# Logging configuration
DEFAULT_LOG_LEVEL = 20  # INFO level
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"

# Memory & chunk size configuration (in MB or rows)
MAX_MEMORY_GB_DEFAULT = 8.0  # Default max recommended file size to process in GB

# Chunk size thresholds by file size (in MB)
CHUNK_SIZE_THRESHOLDS = {
    "small": 50,    # files < 50MB
    "medium": 500,  # files 50MB to < 500MB
    "large": 2000,  # files 500MB to < 2GB
}

# Chunk size row counts
CHUNK_SIZE_VALUES = {
    "small": 50_000,
    "medium": 100_000,
    "large": 200_000,
    "max_rows": 500_000,
}

# Memory usage factor (rows per MB)
MEMORY_USAGE_FACTOR = 0.7

# Estimated rows per MB (approximation)
ROWS_PER_MB = 1000

##########################
# Added for lookup.py usage

# Pattern to normalize column names by replacing non-word characters with underscores
COLUMN_NAME_NORMALIZE_PATTERN = re.compile(r'\W+')

# Supported file extensions for lookup files
SUPPORTED_LOOKUP_EXTENSIONS = (
    ".csv",
    ".parquet",
    ".json",
    ".jsonl",
    ".xls",
    ".xlsx",
)
