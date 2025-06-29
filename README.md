# 🧼 data_cleaner – Universal Data Cleaning & Conversion Toolkit

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/your-username/data_cleaner)

## 📌 Overview

`data_cleaner` is a Python-based CLI and library tool designed for data preprocessing, cleaning, and format conversion. It simplifies ingesting, validating, and profiling structured data files like CSV, Excel, TSV, JSON, and more. It ensures your data is clean and analysis-ready.

## 🚀 Key Features

### ✅ File Validation & Conversion
- Supports `.csv`, `.xlsx`, `.xls`, `.tsv`, `.txt`, `.json`, `.jsonl`, `.parquet`
- Auto-converts to `.csv` when needed
- Intelligent delimiter detection
- Memory-safe processing for large files
- Validates file paths and extensions

### 📊 Column & Header Handling
- Header validation with Unicode & special character support
- Column name normalization (`normalize_column_name`)
- Missing column detection with intelligent suggestions
- Safe column referencing with detailed error messages

### 💡 Performance Tracking
- Step-wise runtime and memory tracking via `PerformanceTracker`
- Context manager (`log_step`) for profiling operations
- System resource logging (CPU, memory, disk)
- Memory monitor for detecting leaks or spikes

### 🧠 Smart Suggestions
- Fuzzy column name matching (`suggest_similar_columns`)
- Helpful CLI error tips (e.g. encoding, delimiter, memory issues)

## 📁 Project Structure

```
data_cleaner/
├── __init__.py
├── cli.py                # CLI entry point
├── converter.py          # File format conversion to CSV
├── utils.py             # Validation, normalization, suggestions
├── perf_utils.py        # Performance tracking & memory monitoring
├── logger_setup.py      # Centralized logger configuration
├── lookup.py            # (Optional) Column mappings / dictionary logic
├── config.py            # Global constants / configs
└── tests/               # Test suite
```

## 🛠 Installation

### From PyPI (Recommended)
```bash
pip install data-cleaner
```

### From Source
```bash
git clone https://github.com/your-username/data_cleaner.git
cd data_cleaner
pip install -e .
```

### Dependencies
- `pandas` - Data manipulation and analysis
- `polars` - High-performance DataFrame library
- `psutil` - System and process utilities
- `openpyxl` - Excel file handling
- `pyarrow` - Parquet file support

## 🔧 Usage

### Command Line Interface

Basic usage:
```bash
python -m data_cleaner.cli --input data.xlsx --output output/ --verbose
```

Advanced usage:
```bash
python -m data_cleaner.cli \
    --input large_dataset.csv \
    --output cleaned/ \
    --delimiter ";" \
    --encoding utf-8 \
    --profile \
    --verbose
```

### CLI Options

| Option | Short | Description |
|--------|-------|-------------|
| `--input` | `-i` | Input file path |
| `--output` | `-o` | Output directory for converted CSV |
| `--delimiter` | `-d` | Custom delimiter for `.txt` or `.tsv` files |
| `--verbose` | `-v` | Enable detailed logs and performance summary |
| `--encoding` | | Optional file encoding (`utf-8`, `latin1`, etc.) |
| `--profile` | | Enable performance profiling and memory logging |
| `--streaming` | | Activate streaming mode (for large datasets, WIP) |

### Python Library Usage

```python
from data_cleaner import DataCleaner, PerformanceTracker
from data_cleaner.utils import normalize_column_name, suggest_similar_columns

# Initialize cleaner
cleaner = DataCleaner()

# Convert file
result = cleaner.convert_file(
    input_path="data.xlsx",
    output_dir="output/",
    delimiter=None,
    encoding="utf-8"
)

# Performance tracking
with PerformanceTracker() as tracker:
    # Your data processing code here
    df = cleaner.load_and_validate("data.csv")
    
print(tracker.get_summary())
```

## 📤 Supported Formats

| Input Format | Output | Notes |
|-------------|--------|-------|
| `.csv` | CSV | Used as-is if valid |
| `.xlsx`, `.xls` | CSV | Converted using `pandas.read_excel` |
| `.tsv`, `.txt` | CSV | Auto-detected or custom delimiter |
| `.json`, `.jsonl` | CSV | `pandas.read_json` with `lines=True` if needed |
| `.parquet` | CSV | Used directly (if `.csv` target not enforced) |

## 🧪 Error Handling

The tool provides robust error handling with helpful suggestions:

- **FileNotFoundError**: Missing or invalid input file path
- **PermissionError**: Inaccessible files
- **ValueError**: Unsupported formats or missing columns
- **RuntimeError**: Conversion or memory-related issues
- **Encoding Issues**: Automatic encoding detection and suggestions
- **Memory Warnings**: Smart file size vs. system memory analysis

## 🛡 Performance & Memory Management

### System Resource Awareness
- Detects file size and system memory
- Warns for large file sizes and low memory
- Calculates optimal chunk sizes for large files
- Real-time memory monitoring during processing

### Performance Profiling
```python
from data_cleaner.perf_utils import log_step

with log_step("Data Loading"):
    df = pd.read_csv("large_file.csv")

with log_step("Data Cleaning"):
    df_cleaned = clean_data(df)
```

## 🧩 Examples

### Basic File Conversion
```bash
# Convert Excel to CSV
python -m data_cleaner.cli -i sales_data.xlsx -o ./output/

# Convert JSON Lines to CSV
python -m data_cleaner.cli -i logs.jsonl -o ./processed/ --verbose
```

### Advanced Processing
```bash
# Large file with custom settings
python -m data_cleaner.cli \
    --input huge_dataset.txt \
    --output processed/ \
    --delimiter "|" \
    --encoding latin1 \
    --profile \
    --streaming
```

### Programmatic Usage
```python
from data_cleaner import DataCleaner
from data_cleaner.utils import suggest_similar_columns

cleaner = DataCleaner()

# Convert and validate
try:
    result = cleaner.convert_file("messy_data.xlsx", "clean/")
    print(f"✅ Converted successfully: {result['output_path']}")
except ValueError as e:
    # Get smart suggestions for missing columns
    suggestions = suggest_similar_columns("problematic_column", df.columns)
    print(f"❌ Error: {e}")
    print(f"💡 Did you mean: {suggestions}")
```

## 🧪 Testing

Run the test suite:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=data_cleaner --cov-report=html
```

## 👨‍💻 Development

### Setup Development Environment
```bash
git clone https://github.com/your-username/data_cleaner.git
cd data_cleaner
pip install -e ".[dev]"
```

### Code Style
This project uses:
- `black` for code formatting
- `flake8` for linting
- `mypy` for type checking

```bash
# Format code
black data_cleaner/

# Run linting
flake8 data_cleaner/

# Type checking
mypy data_cleaner/
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📚 [Documentation](https://github.com/your-username/data_cleaner/wiki)
- 🐛 [Issue Tracker](https://github.com/your-username/data_cleaner/issues)
- 💬 [Discussions](https://github.com/your-username/data_cleaner/discussions)

## 🏆 Acknowledgments

- Built with `pandas`, `polars`, and `psutil`
- Inspired by the need for robust, production-ready data preprocessing
- Thanks to all contributors and the open-source community

---

**Made with ❤️ for data scientists and engineers who value clean, reliable data.**
