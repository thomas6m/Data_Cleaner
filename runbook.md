# Data Cleaner CLI Tool Setup Guide

## Environment Setup

### Create Virtual Environment
```bash
mkdir -p data_cleaner/python-env
python -m venv data_cleaner/python-env
source data_cleaner/python-env/python-env/bin/activate   # On Linux/macOS
python -m pip install --upgrade pip
```

### Create Requirements File
```bash
tee requirements.txt <<EOD
# Core data processing
pandas>=1.5.3
polars>=0.20.0
# Excel support
openpyxl>=3.1.2
xlrd>=2.0.1
# JSON, parquet, and Excel IO
pyarrow>=14.0.1
# Logging (with colored output)
coloredlogs>=15.0.1
# System metrics
psutil>=5.9.8
# Argument parsing enhancements (optional)
argcomplete>=3.1.1  # If using tab-completion in shell
# Optional: If reading xlsx in pandas throws errors
et_xmlfile>=1.1.0
EOD
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Package Setup

### Create setup.py
```python
from setuptools import setup, find_packages

setup(
    name="data_cleaner",
    version="0.1.0",
    description="🧼 A CLI tool for cleaning and enriching CSV/Excel data with deduplication and lookup support.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=1.5.3",
        "polars>=0.20.0",
        "openpyxl>=3.1.2",
        "xlrd>=2.0.1",
        "pyarrow>=14.0.1",
        "coloredlogs>=15.0.1",
        "psutil>=5.9.8",
        "argcomplete>=3.1.1",
        "et_xmlfile>=1.1.0",
    ],
    entry_points={
        "console_scripts": [
            "data-cleaner=data_cleaner.cli:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
)
```

### Install Package in Development Mode
```bash
pip install -e .
```

## CLI Usage

### Command Syntax
```bash
usage: data-cleaner [-h] --input INPUT [--output OUTPUT] [--subset SUBSET]
                    [--keep KEEP | --drop DROP] [--convert-dir CONVERT_DIR]
                    [--lookup LOOKUP] [--lookup-key LOOKUP_KEY]
                    [--lookup-fields LOOKUP_FIELDS] [--dry-run]
                    [--output-format {csv,parquet}] [--num-workers NUM_WORKERS]
                    [--no-cache]
```

### Arguments Description

**Required Arguments:**
- `--input INPUT, -i INPUT`: Input file path (required)

**Optional Arguments:**
- `-h, --help`: Show help message and exit
- `--output OUTPUT, -o OUTPUT`: Output file path (optional)
- `--subset SUBSET, -s SUBSET`: Comma-separated columns for deduplication
- `--keep KEEP, -k KEEP`: Comma-separated columns to keep (mutually exclusive with --drop)
- `--drop DROP, -d DROP`: Comma-separated columns to drop (mutually exclusive with --keep)
- `--convert-dir CONVERT_DIR`: Directory for converted files (default: your default convert dir)
- `--lookup LOOKUP`: Path to lookup file
- `--lookup-key LOOKUP_KEY`: Column to join on for lookup
- `--lookup-fields LOOKUP_FIELDS`: Comma-separated fields to join from lookup
- `--dry-run`: Perform a dry run without writing output
- `--output-format {csv,parquet}`: Output format, default csv
- `--num-workers NUM_WORKERS`: Number of worker threads for parallel processing (default: your default)
- `--no-cache`: Disable caching of the lookup table

### Example Usage
```bash
data-cleaner --input data.xlsx \
             --subset email \
             --lookup countries.csv \
             --lookup-key country_code \
             --lookup-fields country_name,region \
             --output cleaned.csv \
             --output-format csv \
             --num-workers 4
```

## Features

🧼 **Data Cleaning Tool** with support for:
- **Deduplication**: Remove duplicate rows based on specified columns
- **Column Management**: Keep or drop specific columns
- **Data Enrichment**: Join with lookup tables to add additional fields
- **Format Conversion**: Support for CSV, Excel, and Parquet formats
- **Parallel Processing**: Multi-threaded processing for better performance
- **Caching**: Optional caching for lookup tables
- **Dry Run**: Preview changes without modifying files