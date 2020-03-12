#!/usr/bin/bash

py=python3

# ensure the directory exists
if [[ ! -d dist ]];
then
    echo "Directory not found: dist";
    exit 1;
fi

# ensure there is something to publish
if [[ $(ls dist/*.whl | wc -l) -eq 0 ]];
then
    echo "No wheels found in directory: dist";
    exit 1;
fi

# ensure twine is installed
if [[ $($py -m pip list | grep -E '^twine' | wc -l ) -eq 0 ]];
then
    echo "Required module not found: twine";
    exit 1;
fi

$py -m twine upload dist/*.whl
