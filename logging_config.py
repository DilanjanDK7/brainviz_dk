"""
Logging configuration for BrainViz_DK.

Provides consistent logging across the package with appropriate levels
and formatting for different use cases.
"""

import logging
import sys
from typing import Optional


def setup_logging(
    level: str = "INFO",
    verbose: bool = False,
    quiet: bool = False
) -> logging.Logger:
    """
    Set up logging configuration for BrainViz_DK.
    
    Args:
        level: Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR')
        verbose: Enable verbose logging (DEBUG level)
        quiet: Disable all logging except errors
        
    Returns:
        Configured logger instance
    """
    # Determine log level
    if quiet:
        log_level = logging.ERROR
    elif verbose:
        log_level = logging.DEBUG
    else:
        log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Create logger
    logger = logging.getLogger('brainviz_dk')
    logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    # Create formatter
    if verbose:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
    else:
        formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance for the given name.
    
    Args:
        name: Logger name (defaults to 'brainviz_dk')
        
    Returns:
        Logger instance
    """
    if name is None:
        name = 'brainviz_dk'
    return logging.getLogger(name)


# Default logger instance
logger = get_logger()


class ProgressLogger:
    """Logger for progress messages that can be controlled by verbosity."""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = get_logger('brainviz_dk.progress')
    
    def info(self, message: str) -> None:
        """Log info message."""
        if self.verbose:
            self.logger.info(message)
        else:
            print(f"ℹ️  {message}")
    
    def success(self, message: str) -> None:
        """Log success message."""
        print(f"✓ {message}")
    
    def warning(self, message: str) -> None:
        """Log warning message."""
        print(f"⚠️  {message}")
    
    def error(self, message: str) -> None:
        """Log error message."""
        print(f"❌ {message}")
    
    def debug(self, message: str) -> None:
        """Log debug message."""
        if self.verbose:
            self.logger.debug(message)
