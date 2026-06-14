#!/usr/bin/env bash

# Run makefile
# So, that the AI Dosn't have to remember
# bash code.

if [[ -f Makefile ]]; then
    echo "Makefile found."
else
    echo "No Makefile found in the current directory."
    exit 1
fi

usage() {
    echo "Usage: $0 [-c] [-b] [-d]"
    echo "Options:"
    echo "  -c   Clean the build artifacts."
    echo "  -b   Build the project."
    echo "  -d   Install dependencies."
    exit 1
}

while getopts "cbd" opt; do
    case "$opt" in
        c) make clean ;;
        b) make all ;;
        d) make deps ;
        *) usage ;;
    esac
done