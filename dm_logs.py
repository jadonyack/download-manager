"""
Logging module for the Download Manager

Written by Jadon Yack
"""

import logging

class dm_logger_t:
    def dm_logs_init(self):
        """Initialize logger."""
        self.dm_logger = logging.getLogger('dm_logger')
        self.dm_logger.setLevel(logging.INFO)

        dm_console = logging.StreamHandler()
        dm_logfile = logging.FileHandler('dm.log')

        dm_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        dm_console.setFormatter(dm_format)
        dm_logfile.setFormatter(dm_format)

        self.dm_logger.addHandler(dm_console)
        self.dm_logger.addHandler(dm_logfile)

        self.dm_logger.info('Logger initialized.')

    def dm_log_info(self, string: str):
        """Print info log."""
        self.dm_logger.info(string)

    def dm_log_err(self, string: str):
        """Print error log."""
        self.dm_logger.error(string)

    def dm_log_debug(self, string: str):
        """Print debug log."""
        self.dm_logger.debug(string)

    def __init__(self):
        self.dm_logs_init()
