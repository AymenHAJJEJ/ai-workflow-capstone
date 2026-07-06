"""
run_tests.py

Run all unit tests for the AAVAIL AI Workflow Capstone.
"""

import unittest
import sys


def main():
    """
    Discover and run all tests in the tests directory.
    """

    loader = unittest.TestLoader()

    suite = loader.discover("tests")

    runner = unittest.TextTestRunner(
        verbosity=2
    )

    result = runner.run(suite)

    if result.wasSuccessful():
        print("\n===================================")
        print(" ALL TESTS PASSED")
        print("===================================")
        sys.exit(0)
    else:
        print("\n===================================")
        print(" SOME TESTS FAILED")
        print("===================================")
        sys.exit(1)


if __name__ == "__main__":
    main()