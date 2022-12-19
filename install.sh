#!/bin/zsh
BASEDIR=$(dirname "$0")

if [ -d "$BASEDIR/venv" ]; then
  echo "$BASEDIR/venv is exists"
else
  cd $BASEDIR && python3 -m venv $BASEDIR/venv && source $BASEDIR/venv/activate && pip3 install -r requirements.txt
fi
