# converter.py - File format converter and validator for data_cleaner

This module provides utilities to:
- Validate file paths and formats
- Check system memory resources before processing large files
- Convert various file formats (Excel, TSV, JSON, TXT) to CSV for standardized processing

## Supported Input Formats

- `.csv`
- `.parquet`
- `.xls` / `.xlsx` (Excel)
- `.tsv` (Tab-separated)
- `.txt` (Flexible delimiter: auto-detected or user-defined)
- `.json` / `.jsonl`

## Main Functions

### 1. `convert_to_csv_if_needed(input_path, output_dir, delimiter)`
- Converts a supported input file to CSV format if necessary.
- Returns the path to the converted (or original) CSV file.

### 2. `validate_file_path(file_path, allowed_extensions)`
- Validates that the input file exists, is accessible, and has an allowed extension.

### 3. `check_system_resources(file_path, max_memory_gb)`
- Logs warnings if the input file is too large or system memory is low.

## Error Handling

- Raises `FileNotFoundError` if the file doesn't exist
- Raises `PermissionError` if the file cannot be read
- Raises `ValueError` for unsupported formats
- Raises `RuntimeError` if conversion fails due to parsing, memory, or formatting issues

## Tips & Logging

- Logs format issues and common causes like encoding, memory, or delimiter problems
- Provides suggestions for alternative encodings or delimiters if errors are encountered

## Example Usage

```python
from data_cleaner.converter import convert_to_csv_if_needed
csv_path = convert_to_csv_if_needed("raw_data.xlsx")
```

## Dependencies

- pandas
- psutil