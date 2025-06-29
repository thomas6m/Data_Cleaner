# data_cleaner/cli.py

import argparse
import re
import os
import time
from data_cleaner.converter import convert_to_csv_if_needed
from data_cleaner.polars_cleaner import remove_duplicates_polars
from data_cleaner.utils import validate_header_line
from data_cleaner.logger_setup import setup_logging
from data_cleaner.perf_utils import log_step

logger = setup_logging()

def normalize_list(lst):
    """Normalize a list of column names: strip, lowercase, replace non-word chars with underscores."""
    return [re.sub(r'\W+', '_', s.strip().lower()) for s in lst]

def main():
    parser = argparse.ArgumentParser(
        description="🧼 Clean CSV/Excel files with deduplication, filtering, and enrichment",
        epilog="""Example: data-cleaner --input sample.xlsx --subset Email --lookup lookup.csv --lookup-key Email --lookup-fields User_Type,Region"""
    )
    parser.add_argument("--input", "-i", required=True, help="Input file path")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--subset", "-s", help="Comma-separated columns for deduplication")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--keep", "-k", help="Comma-separated columns to keep")
    group.add_argument("--drop", "-d", help="Comma-separated columns to drop")
    parser.add_argument("--convert-dir", default="./converted", help="Directory for converted files")
    parser.add_argument("--lookup", help="Path to lookup file")
    parser.add_argument("--lookup-key", help="Column to join on")
    parser.add_argument("--lookup-fields", help="Comma-separated fields to join from lookup")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without writing output")
    parser.add_argument("--output-format", choices=["csv", "parquet"], default="csv")
    parser.add_argument("--num-workers", type=int, default=4, help="Number of worker threads for parallel processing")
    parser.add_argument("--no-cache", action="store_true", help="Disable caching of the lookup table")

    args = parser.parse_args()
    total_start = time.perf_counter()

    # Validate input file existence
    if not os.path.isfile(args.input):
        logger.error(f"Input file does not exist: {args.input}")
        print(f"❌ Input file does not exist: {args.input}")
        return

    try:
        with log_step("Convert to CSV if needed"):
            file_path = convert_to_csv_if_needed(args.input, output_dir=args.convert_dir)
    except Exception as e:
        logger.error(f"Conversion error: {e}")
        print(f"❌ Conversion error: {e}")
        return

    try:
        with log_step("Validate header"):
            with open(file_path, "r", encoding="utf-8") as f:
                header_line = f.readline()
            if not validate_header_line(header_line):
                logger.error("Invalid header format")
                print("❌ Invalid header format.")
                return
    except Exception as e:
        logger.error(f"Failed to read header: {e}")
        print(f"❌ Failed to read header: {e}")
        return

    print("📌 Cleaned header columns:")
    print(", ".join([h.strip() for h in header_line.strip().split(",")]))

    # Normalize and parse column lists
    subset = normalize_list(args.subset.split(",")) if args.subset else None
    keep_only = normalize_list(args.keep.split(",")) if args.keep else None
    drop_fields = normalize_list(args.drop.split(",")) if args.drop else None
    lookup_fields = normalize_list(args.lookup_fields.split(",")) if args.lookup_fields else None
    lookup_key = re.sub(r'\W+', '_', args.lookup_key.strip().lower()) if args.lookup_key else None

    try:
        with log_step("Polars cleaning pipeline"):
            output_path = remove_duplicates_polars(
                file_path=file_path,
                output_path=args.output,
                subset=subset,
                keep_only_fields=keep_only,
                drop_fields=drop_fields,
                lookup_path=args.lookup,
                lookup_key=lookup_key,
                lookup_fields=lookup_fields,
                dry_run=args.dry_run,
                output_format=args.output_format,
                num_workers=args.num_workers,
                use_cache=not args.no_cache,
            )
        if args.dry_run:
            print(f"🔎 Dry run complete! No output file created.")
        else:
            print(f"✅ Cleaning complete! Output saved to: {output_path}")
    except Exception as e:
        logger.error(f"Cleaning error: {e}")
        print(f"❌ Cleaning error: {e}")
        return

    total_time = time.perf_counter() - total_start
    logger.info(f"⏱️ Total runtime: {total_time:.2f} seconds.")

if __name__ == "__main__":
    main()
