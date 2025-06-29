# data_cleaner/cli.py

import argparse
import sys
import polars as pl
from data_cleaner.utils import (
    validate_file_path,
    validate_columns_exist,
    normalize_column_name,
    safe_column_reference,
)
from data_cleaner.perf_utils import log_step, get_performance_tracker, log_system_info
from data_cleaner.logger_setup import setup_logging

logger = setup_logging()

def main():
    parser = argparse.ArgumentParser(
        description="Data Cleaner CLI - Process and clean CSV files efficiently."
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Path to the input CSV file"
    )
    parser.add_argument(
        "--columns",
        nargs="+",
        default=None,
        help="List of columns to validate or process"
    )
    parser.add_argument(
        "--normalize-columns",
        action="store_true",
        help="Normalize column names in the output"
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default=None,
        help="Path to save the cleaned output CSV file"
    )

    args = parser.parse_args()

    try:
        validate_file_path(args.input_file, allowed_extensions=['.csv', '.tsv'])
    except Exception as e:
        logger.error(f"Invalid input file: {e}")
        sys.exit(1)

    with log_step("Load CSV file"):
        try:
            df = pl.read_csv(args.input_file)
            logger.info(f"Loaded {len(df)} rows with columns: {df.columns}")
        except Exception as e:
            logger.error(f"Failed to load CSV: {e}")
            sys.exit(1)

    # Validate columns if provided
    if args.columns:
        try:
            validate_columns_exist(df, args.columns, operation="CLI processing")
        except ValueError as e:
            logger.error(str(e))
            # Suggest similar columns if available
            for col in args.columns:
                try:
                    safe_column_reference(df, col, operation="CLI processing")
                except ValueError as ve:
                    logger.error(ve)
            sys.exit(1)

    # Normalize column names if requested
    if args.normalize_columns:
        with log_step("Normalize column names"):
            normalized_cols = [normalize_column_name(c) for c in df.columns]
            df.columns = normalized_cols
            logger.info(f"Normalized columns: {normalized_cols}")

    # Save output if specified
    if args.output_file:
        try:
            validate_file_path(args.output_file, allowed_extensions=['.csv', '.tsv'])
        except ValueError:
            # File might not exist yet, so skip existence check
            ext = args.output_file.split('.')[-1].lower()
            if ext not in ['csv', 'tsv']:
                logger.error("Output file must have .csv or .tsv extension")
                sys.exit(1)

        with log_step("Save cleaned CSV"):
            try:
                df.write_csv(args.output_file)
                logger.info(f"Saved cleaned data to {args.output_file}")
            except Exception as e:
                logger.error(f"Failed to save output file: {e}")
                sys.exit(1)

    tracker = get_performance_tracker()
    tracker.log_summary()

if __name__ == "__main__":
    log_system_info()
    main()