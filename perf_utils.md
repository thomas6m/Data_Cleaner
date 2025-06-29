# perf_utils.py - Performance Monitoring Utilities for data_cleaner

This module provides utilities to track performance metrics, monitor memory usage, log step durations, and collect system resource information throughout the data cleaning pipeline.

## Key Components

### 1. PerformanceTracker

A class to record execution time and memory usage for multiple steps.

**Methods:**
- `.record_step(step_name, duration, memory_delta, memory_current)`
- `.get_summary() -> Dict`
- `.log_summary()`

### 2. Context Managers

#### `log_step(step_name: str, track_globally: bool = True)`
Logs duration and memory usage for any step. Automatically adds emojis based on speed/memory.

#### `memory_monitor(warning_threshold_mb: float = 1000)`
Tracks memory usage of a block and logs a warning if growth exceeds threshold.

### 3. System and File Resource Checks

#### `log_system_info()`
Logs CPU, memory, and disk usage stats. Called once by log_step automatically.

#### `check_system_resources(file_path: str, max_memory_gb: float = 8.0) -> Dict`
Analyzes file size vs. system memory to determine chunk sizes or streaming recommendations.

### 4. Utilities

#### Global Tracker Management
- `get_performance_tracker()` - Access the global performance tracker instance
- `reset_performance_tracker()` - Reset the global performance tracker instance

#### Formatting
- `format_duration(seconds: float) -> str` - Converts raw durations into human-readable formats (ms, s, m, h)

## Usage Examples

```python
from data_cleaner.perf_utils import log_step, get_performance_tracker

with log_step("Load data"):
    df = read_large_file("data.csv")

tracker = get_performance_tracker()
tracker.log_summary()
```

## Dependencies

- **psutil**: for system and process memory usage
- **os, time, contextlib**: standard library modules
- **data_cleaner.logger_setup**: centralized logging