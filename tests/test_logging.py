"""
test_logging.py

Unit tests for the logging system.
"""

import os
import logging
import unittest

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "api.log")


class TestLogging(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Configure test logger."""

        os.makedirs(LOG_DIR, exist_ok=True)

        logging.basicConfig(
            filename=LOG_FILE,
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            force=True
        )

    def test_log_file_created(self):
        """Log file should be created."""

        logging.info("Creating log file for testing.")

        self.assertTrue(os.path.exists(LOG_FILE))

    def test_write_log(self):
        """Writing to the log should succeed."""

        message = "Unit test log message"

        logging.info(message)

        with open(LOG_FILE, "r") as f:
            content = f.read()

        self.assertIn(message, content)

    def test_multiple_log_entries(self):
        """Multiple log entries should be recorded."""

        logging.info("Entry One")
        logging.info("Entry Two")

        with open(LOG_FILE, "r") as f:
            content = f.read()

        self.assertIn("Entry One", content)
        self.assertIn("Entry Two", content)

    def test_log_not_empty(self):
        """Log file should contain data."""

        self.assertGreater(os.path.getsize(LOG_FILE), 0)


if __name__ == "__main__":
    unittest.main()