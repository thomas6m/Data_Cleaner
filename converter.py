# data_cleaner/converter.py
import os
import pandas as pd
import psutil
from typing import Optional
from data_cleaner.logger_setup import setup_logging

logger = setup_logging()

def check_system_resources(file_path: str, max_memory_gb: float = 8.0):
    """Check if system has enough resources to process file"""
    if not os.path.exists(file_path):
        return True  # Will be caught by later validation
    
    file_size = os.path.getsize(file_path) / (1024**3)  # GB
    available_memory = psutil.virtual_memory().available / (1024**3)  # GB
    
    if file_size > max_memory_gb:
        logger.warning(f"⚠️ Large file detected: {file_size:.2f}GB. Consider using streaming mode.")
    
    if available_memory < (file_size * 2):
        logger.warning(f"⚠️ Low memory: {available_memory:.2f}GB available for {file_size:.2f}GB file.")
    
    return True

def validate_file_path(file_path: str, allowed_extensions: list = None) -> bool:
    """Validate file path for security and accessibility"""
    if not file_path or '..' in file_path:
        return False
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file does not exist: {file_path}")
    
    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"Cannot read input file: {file_path}")
    
    if allowed_extensions:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in allowed_extensions:
            raise ValueError(f"File extension {ext} not in allowed extensions: {allowed_extensions}")
    
    return True

def convert_to_csv_if_needed(input_path: str, output_dir: str = "./converted", delimiter: Optional[str] = None) -> str:
    """
    Convert various file formats to CSV if needed.
    
    Args:
        input_path: Path to input file
        output_dir: Directory to save converted files
        delimiter: Custom delimiter for text files
    
    Returns:
        Path to CSV file (original or converted)
    
    Raises:
        FileNotFoundError: If input file doesn't exist
        PermissionError: If file cannot be read
        ValueError: If file format is unsupported
        RuntimeError: If conversion fails
    """
    # Validate input file
    allowed_extensions = ['.csv', '.xlsx', '.xls', '.txt', '.tsv', '.parquet', '.json', '.jsonl']
    validate_file_path(input_path, allowed_extensions)
    
    # Check system resources
    check_system_resources(input_path)
    
    _, ext = os.path.splitext(input_path)
    ext = ext.lower()
    
    # Skip conversion for already supported formats
    if ext in [".csv", ".parquet"]:
        logger.info(f"ℹ️ Skipping conversion. File already in supported format: {input_path}")
        return input_path
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output path
    name_only = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(output_dir, f"{name_only}.converted.csv")
    
    try:
        logger.info(f"🔄 Converting {ext} file to CSV: {input_path}")
        
        if ext in [".xls", ".xlsx"]:
            # Handle Excel files
            df = pd.read_excel(input_path)
            logger.info(f"📊 Loaded Excel file: {df.shape[0]} rows, {df.shape[1]} columns")
            
        elif ext == ".txt":
            # Handle text files with custom or auto-detected delimiter
            try:
                df = pd.read_csv(input_path, sep=delimiter or None, engine="python")
            except Exception as e:
                # Try common delimiters if auto-detection fails
                for sep in ['\t', ';', '|']:
                    try:
                        df = pd.read_csv(input_path, sep=sep, engine="python")
                        logger.info(f"📝 Detected delimiter: '{sep}'")
                        break
                    except:
                        continue
                else:
                    raise e
                    
        elif ext == ".tsv":
            # Handle TSV files
            df = pd.read_csv(input_path, sep="\t")
            
        elif ext in [".json", ".jsonl"]:
            # Handle JSON files
            if ext == ".json":
                df = pd.read_json(input_path)
            else:  # .jsonl
                df = pd.read_json(input_path, lines=True)
            
        else:
            supported_formats = ", ".join(allowed_extensions)
            raise ValueError(f"Unsupported file type: {ext}. Supported formats: {supported_formats}")
        
        # Validate loaded data
        if df.empty:
            raise ValueError(f"File appears to be empty or contains no valid data: {input_path}")
        
        # Write to CSV
        df.to_csv(output_path, index=False)
        logger.info(f"✅ Successfully converted to CSV: {output_path}")
        logger.info(f"📊 Final output: {df.shape[0]} rows, {df.shape[1]} columns")
        
        return output_path
        
    except FileNotFoundError:
        raise
    except PermissionError:
        raise
    except Exception as e:
        error_msg = f"Failed to convert file '{input_path}': {str(e)}"
        logger.error(f"❌ {error_msg}")
        
        # Provide helpful suggestions based on error type
        if "codec" in str(e).lower() or "encoding" in str(e).lower():
            logger.info("💡 Tip: Try specifying a different encoding (UTF-8, latin-1, etc.)")
        elif "delimiter" in str(e).lower() or "separator" in str(e).lower():
            logger.info("💡 Tip: Try specifying a custom delimiter with --delimiter option")
        elif "memory" in str(e).lower():
            logger.info("💡 Tip: File might be too large. Consider splitting it into smaller chunks")
        
        raise RuntimeError(error_msg)