#!/bin/zsh
BASEDIR=$(dirname "$0")

source "$BASEDIR/venv/bin/activate" && pip3 install -r "$BASEDIR/requirements.txt" && python3 "$BASEDIR/main.py" $1