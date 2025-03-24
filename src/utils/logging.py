"""Logging utilities for the GivingTuesday Campaign Advisor."""

import logging
import sys
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler

from src.utils.config import config

# Setup console for rich output
console = Console()


def setup_logging(name: str = "gt_campaign_advisor", level: Optional[str] = None) -> logging.Logger:
    """Set up logging with the specified level.
    
    Args:
        name: Name of the logger.
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            Defaults to value in config.
            
    Returns:
        Configured logger instance.
    """
    log_level = level or config.log_level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Configure logging with rich handler
    logging.basicConfig(
        level=numeric_level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)]
    )
    
    return logging.getLogger(name)


# Create logger instance
logger = setup_logging()
