#!/bin/zsh
BASEDIR=$(dirname "$0")

source "$BASEDIR/venv/bin/activate" && python3 "$BASEDIR/main.py" $1