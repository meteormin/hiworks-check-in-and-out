#!/bin/zsh
BASEDIR=$(dirname "$0")

cd $BASEDIR && source "$BASEDIR/venv/bin/activate" && python3 "$BASEDIR/cli.py" $1