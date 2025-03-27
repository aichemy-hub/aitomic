"""This module sets up the logging for the aitomic package.

The logger can be used in other modules like this:
  from aitomic.aitomic_logging import logger
  logger.error("This is an error")
  logger.warning("This is a warning")
  logger.info("This is an info")
  logger.debug("This is a debug")
  logger.critical("This is a critical")
"""

import logging

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler("aitomic.log")
c_handler.setLevel(logging.INFO)
f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
f_format = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)
