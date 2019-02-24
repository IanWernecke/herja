"""Execute a reset, a get, or a set command for various settings."""


import logging
import os

from . import Settings, SETTINGS_PATH
from ..decorators import MainCommands


@MainCommands(
    ('reset', 'Reset the configuration settings by deleting the settings file.', []),
    ('get', 'Get a value from stored settings.', [
        (['key'], {'help': 'The name of the value to obtain from settings.'})
    ]),
    ('set', 'Set a value to be stored in settings.', [
        (['key'], {'help': 'The name of the value to save in settings.'}),
        (['value'], {'help': 'The value of the key to be stored in settings.'})
    ])
)
def main(args):
    """Handle arguments given to this module."""
    # remove the current configuration file, if it exists
    if args.command == 'reset':
        logging.info('Ensuring log does not exist: "%s"', SETTINGS_PATH)
        if os.path.isfile(SETTINGS_PATH):
            logging.info('Removing log: "%s"', SETTINGS_PATH)
            os.remove(SETTINGS_PATH)
        return 0

    # get a configuration value
    if args.command == 'get':

        with Settings() as settings:
            result = settings.get(args.key, None)

        if result is None:
            logging.warning('Failed to obtain value for key: "%s"', args.key)
            return 1

        logging.info('Obtained value from settings: "%s"', result)
        return 0

    # set a configuration value
    if args.command == 'set':

        with Settings() as settings:
            settings[args.key] = args.value

        with Settings() as settings:
            result = settings.get(args.key, None)

        assert result == args.value, 'Invalid result obtained: "{0}"'.format(result)
        return 0

    return 1
