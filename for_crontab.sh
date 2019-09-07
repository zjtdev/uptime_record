#!/bin/bash
# https://stackoverflow.com/questions/4150671/how-to-set-virtualenv-for-a-crontab

CURRDIR=`dirname "$0"`
BASEDIR=`cd "$CURRDIR"; pwd`

VENV_ACTIVATE="$BASEDIR"/venv/bin/activate
PYTHON_CMD="$BASEDIR"/uptime_record.py

cd "$BASEDIR"
source "$VENV_ACTIVATE"
python3 "$PYTHON_CMD"
