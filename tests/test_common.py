"""Pytest module for testing the functionality of the herja.common module."""


import os
from herja.common import execute


def test_execute(logger):
    """Ensure execute is able to find the current file when this directory is listed."""
    abs_file = os.path.abspath(__file__)
    file_dir, file_name = os.path.split(abs_file)

    stdout, stderr, code = execute(['ls', '-halp', file_dir])

    encoded_name = file_name.encode()
    assert any(line.endswith(encoded_name) for line in stdout.splitlines())
