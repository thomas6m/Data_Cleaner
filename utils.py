# data_cleaner/utils.py
import re
import os
import polars as pl
from typing import List, Optional

def validate_header_line(header: str) -> bool:
    """
    Validates a CSV header line to ensure it contains only expected characters.
    
    Allowed characters:
    - Alphanumeric characters
    - Underscores (_), hyphens (-), periods (.), commas (,)
    - At symbols (@), parentheses (), brackets [], braces {}
    - Colons (:), semicolons (;), quotes (' ")
    - Spaces and Unicode characters (e.g., accented letters, non-English)
    
    Args:
        header: The header line to validate
        
    Returns:
        bool: True if header is valid, False otherwise
    """
    if not header or not header.strip():
        return False
    
    # Enhanced regex to allow more characters commonly found in CSV headers
    # Including parentheses, brackets, quotes, and other punctuation
    pattern = r"^[\w\s,.\-@()[\]{}:;'\"+=<>?/\\*&%$#!~`|]+$"
    
    return bool(re.match(pattern, header.strip(), flags=re.UNICODE))

def validate_file_path(file_path: str, allowed_extensions: List[str] = None) -> bool:
    """
    Validate file path for security and accessibility.
    
    Args:
        file_path: Path to validate
        allowed_extensions: List of allowed file extensions (with dots)
        
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If path is invalid or extension not allowed
        FileNotFoundError: If file doesn't exist
        PermissionError: If file cannot be read
    """
    if not file_path or '..' in file_path:
        raise ValueError("Invalid file path: path is empty or contains '..'")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File does not exist: {file_path}")
    
    if not os.access(file_path, os.R_OK):
        raise PermissionError(f"Cannot read file: {file_path}")
    
    if allowed_extensions:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in allowed_extensions:
            raise ValueError(
                f"File extension '{ext}' not allowed. "
                f"Supported extensions: {', '.join(allowed_extensions)}"
            )
    
    return True

def validate_columns_exist(df: pl.DataFrame, columns: List[str], operation: str) -> None:
    """
    Validate that specified columns exist in the dataframe.
    
    Args:
        df: Polars DataFrame to check
        columns: List of column names to validate
        operation: Description of the operation (for error messages)
        
    Raises:
        ValueError: If any columns are missing
    """
    if not columns:
        return
    
    missing = [col for col in columns if col not in df.columns]
    
    if missing:
        available = list(df.columns)
        raise ValueError(
            f"Missing columns for {operation}: {missing}. "
            f"Available columns: {available}"
        )

def normalize_column_name(col: str) -> str:
    """
    Normalize column names to a consistent format.
    
    Args:
        col: Column name to normalize
        
    Returns:
        str: Normalized column name (lowercase, non-alphanumeric replaced with underscores)
    """
    if not col:
        return ""
    
    # Replace non-word characters with underscores, convert to lowercase
    normalized = re.sub(r'\W+', '_', col.strip().lower())
    
    # Remove leading/trailing underscores
    normalized = normalized.strip('_')
    
    # Ensure it doesn't start with a number
    if normalized and normalized[0].isdigit():
        normalized = f"col_{normalized}"
    
    # Handle empty strings after normalization
    if not normalized:
        normalized = "unnamed_column"
    
    return normalized

def suggest_similar_columns(target: str, available: List[str], max_suggestions: int = 3) -> List[str]:
    """
    Suggest similar column names based on string similarity.
    
    Args:
        target: The column name that wasn't found
        available: List of available column names
        max_suggestions: Maximum number of suggestions to return
        
    Returns:
        List of suggested column names
    """
    if not available:
        return []
    
    # Simple similarity based on common substrings and edit distance
    def similarity_score(a: str, b: str) -> float:
        a, b = a.lower(), b.lower()
        
        # Exact match
        if a == b:
            return 1.0
        
        # Substring match
        if a in b or b in a:
            return 0.8
        
        # Common words/tokens
        a_tokens = set(re.split(r'[_\s]+', a))
        b_tokens = set(re.split(r'[_\s]+', b))
        common = len(a_tokens & b_tokens)
        total = len(a_tokens | b_tokens)
        
        if total == 0:
            return 0.0
        
        return common / total
    
    # Calculate similarity scores
    scores = [(col, similarity_score(target, col)) for col in available]
    
    # Sort by similarity and filter out very low scores
    scores = [(col, score) for col, score in scores if score > 0.2]
    scores.sort(key=lambda x: x[1], reverse=True)
    
    return [col for col, _ in scores[:max_suggestions]]

def safe_column_reference(df: pl.DataFrame, column: str, operation: str = "") -> str:
    """
    Safely reference a column with helpful error messages if it doesn't exist.
    
    Args:
        df: Polars DataFrame
        column: Column name to reference
        operation: Description of operation for error context
        
    Returns:
        str: The column name if it exists
        
    Raises:
        ValueError: If column doesn't exist, with suggestions
    """
    if column in df.columns:
        return column
    
    # Column doesn't exist, provide helpful error
    available = list(df.columns)
    suggestions = suggest_similar_columns(column, available)
    
    error_msg = f"Column '{column}' not found"
    if operation:
        error_msg += f" for {operation}"
    
    error_msg += f". Available columns: {available}"
    
    if suggestions:
        error_msg += f". Did you mean: {suggestions}?"
    
    raise ValueError(error_msg)

def get_memory_usage_mb() -> float:
    """Get current memory usage in MB."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"

def calculate_optimal_chunk_size(file_size_mb: float, available_memory_mb: float) -> int:
    """
    Calculate optimal chunk size based on file size and available memory.
    
    Args:
        file_size_mb: Size of file in MB
        available_memory_mb: Available memory in MB
        
    Returns:
        int: Optimal chunk size in rows
    """
    if file_size_mb < 50:
        return 25_000
    elif file_size_mb < 200:
        return 50_000
    elif file_size_mb < 1000:
        return 100_000
    else:
        # For very large files, use conservative chunk size
        # Aim to use at most 20% of available memory per chunk
        memory_based_rows = int((available_memory_mb * 0.2) * 100)  # rough estimate: 100 rows per MB
        return min(max(memory_based_rows, 50_000), 500_000)  # Between 50k and 500k rows