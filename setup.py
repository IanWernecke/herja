"""This file is used for creating and installing the package."""

import os
from setuptools import setup, find_packages

setup(
    name='herja',
    version='0.0.4',
    author='IanWernecke',
    author_email='IanWernecke@protonmail.com',
    description='A package for handling common utilities.',
    license='GPLv3',
    keywords='common utility decorators Main MainCommands',
    url='http://github.com/IanWernecke/herja',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests'
    ]
)
