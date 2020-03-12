"""A module for testing the features of herja.logging features."""

import logging
from herja.common import get_logger


def test_default_logger():
    """Ensure the default logger obtained is actually a standard logging logger."""
    assert isinstance(get_logger(), logging.Logger)
