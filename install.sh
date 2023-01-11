#!/bin/zsh
BASEDIR=$(dirname "$0")

if [ -d "$BASEDIR/venv" ]; then
  echo "$BASEDIR/venv is exists"
else
  cd $BASEDIR && python3 -m venv "$BASEDIR/venv"
fi

source "$BASEDIR/venv/bin/activate" && pip install -r requirements.txt