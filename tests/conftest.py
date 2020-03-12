"""Pytest special file for fixtures and features."""


from herja.common import get_logger
import pytest


@pytest.fixture(scope='session')
def logger():
    return get_logger()
