# flags.py

import logging

# Set up logging to capture flagged methods
logging.basicConfig(level=logging.WARNING)


def potential_performance_flag(method):
    """
    A decorator that flags methods as potentially inefficient.
    """
    method.is_flagged_for_performance_check = True
    return method
