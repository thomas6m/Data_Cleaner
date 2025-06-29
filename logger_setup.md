# logger_setup.py - Logging Configuration for data_cleaner

This module configures and returns a logger specifically for the `data_cleaner` project.
It uses `coloredlogs` to display colored, human-readable log messages in the terminal.

## Key Features

- Applies a consistent log format across the project
- Clears duplicate handlers to prevent double logging
- Uses colored output for easier debugging
- Configurable via `config.py` (log level and format)

## Functions

### setup_logging(level: int = DEFAULT_LOG_LEVEL) -> logging.Logger

Initializes and returns a logger instance for the module.

## Example

```python
from data_cleaner.logger_setup import setup_logging
logger = setup_logging()
logger.info("This is a test log with colored output.")
```

## Configuration

- **DEFAULT_LOG_LEVEL**: Default log level (e.g., logging.INFO)
- **LOG_FORMAT**: Log message format string (timestamp, level, message)

## Dependencies

- logging
- coloredlogs
- sys
- data_cleaner.config