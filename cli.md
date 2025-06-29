# CLI module for data_cleaner

This script provides a command-line interface for processing and cleaning tabular data files (CSV, Excel, JSON, etc.) using Polars. It supports conversion, validation, deduplication, column filtering, and data enrichment using lookup files.

## Features

- Auto-convert Excel, JSON, TSV, or Parquet to CSV if needed.
- Header validation to ensure proper column structure.
- Duplicate row removal using subset columns.
- Column selection: keep or drop specific fields.
- Optional lookup join (enrichment) from an external reference file.
- Support for dry run (no write) and multi-threaded processing.
- Output as CSV or Parquet.

## Command-line Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `--input` | `-i` | Path to input file (required) |
| `--output` | `-o` | Path to output file (optional) |
| `--subset` | `-s` | Comma-separated column names for deduplication |
| `--keep` | `-k` | Comma-separated column names to keep |
| `--drop` | `-d` | Comma-separated column names to drop |
| `--convert-dir` | | Directory to save temporary converted files |
| `--lookup` | | Path to lookup file for enrichment |
| `--lookup-key` | | Column to join on from both datasets |
| `--lookup-fields` | | Comma-separated fields to fetch from lookup file |
| `--dry-run` | | If set, no output file will be written |
| `--output-format` | | Output format: csv or parquet (default: csv) |
| `--num-workers` | | Number of worker threads (default: 4) |
| `--no-cache` | | Disable caching of the lookup file |

## Example

```bash
data-cleaner --input data.xlsx --subset email \
    --lookup users.csv --lookup-key email --lookup-fields user_type,region
```

## Dependencies

- Polars
- pandas (for Excel reading)
- Python 3.8+