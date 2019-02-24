import logging
import os

from . import execute
from .decorators import MainCommands


@MainCommands(
    ('mu-list', 'List events for a specified meetup group.', [
        (['group'], {'help': 'The name of the group whose events to read.'})
    ])
)
def main(args):
    """Handle arguments given to this module."""
    execute(['ls', '..'])
    execute(['ls', '../haha *.txt'])
    return 0
