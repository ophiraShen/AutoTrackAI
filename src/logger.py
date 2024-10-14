# src/logger.py

from loguru import logger
import sys


# Configure loguru
logger.remove()
logger.add(sys.stdout, level="DEBUG", format="{time} {level} {message}", colorize=True)
logger.add("logs/app.log", rotation="1 MB", level="DEBUG")

# Aias the logger for easier import
LOG = logger

# Make the logger available for import with the alias
__all__ = ["LOG"]