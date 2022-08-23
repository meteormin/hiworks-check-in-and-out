#!/bin/zsh
BASEDIR=$(dirname "$0")

source "$BASEDIR/venv/bin/activate" && python3 main.py $1