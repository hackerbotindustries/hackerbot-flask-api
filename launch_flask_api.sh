#!/bin/bash
################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.26
#
# This script launches the Hackerbot Flask API process and occupies the serial port.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


set -o pipefail

BASE_DIR="$(pwd)"

cd $HOME/hackerbot/hackerbot-flask-api/

# export FLASK_APP=$HOME/hackerbot/hackerbot-flask-api/app/run.py
export FLASK_APP=app/run.py


# Log directory setup
timestamp_flask="hackerbot_flask_$(date '+%Y%m%d%H%M')"
logdir="$HOME/hackerbot/logs"

# Create log directory if it doesn't exist
if [ ! -d "$logdir" ]; then
    echo "Creating log directory at $logdir"
    mkdir -p "$logdir"
fi

# Keep only the latest 5 logs
ls -1dt "$logdir"/* | tail -n +6 | xargs rm -rf 2>/dev/null

logfile_backend="$logdir/$timestamp_flask.txt"

# Port configuration
FLASK_PORT=5000
LOCAL_IP=$(hostname -I | awk '{print $1}')

function echo_failure {
    echo ""
    echo "---------------------------------------------"
    echo "FAILURE! Hackerbot flask api failed to launch."
    echo "Check logs in: $logfile_backend"
    echo "---------------------------------------------"
    exit 1
}

echo "---------------------------------------------"
echo "STARTING HACKERBOT FLASK API"
echo "---------------------------------------------"

# Stop existing processes first
if command -v stop-flask-api >/dev/null 2>&1; then
    echo "Cleaning up existing process"
    if ! stop-flask-api >> "$logfile_backend" 2>&1; then
        echo "Failed to execute cleanup..."
    fi
else
    echo "stop-flask-api command not found. Skipping cleanup."
fi


# Start Flask Backend
# FLASK_APP=app.py FLASK_ENV=development flask run --host=0.0.0.0 --port=$FLASK_PORT --no-debugger --no-reload >> "$logfile_backend" 2>&1 &
FLASK_ENV=development flask run --host=0.0.0.0 --port=$FLASK_PORT --no-debugger --no-reload >> "$logfile_backend" 2>&1 &
PID_BACKEND=$!


# Wait a few seconds for processes to start
sleep 5

# Check if processes are running
if ! ps -p $PID_BACKEND > /dev/null; then
    echo "Flask backend failed to start!"
    echo_failure
fi

echo ""
echo "---------------------------------------------"
echo "SUCCESS! Hackerbot Web Application is Running!"
echo "Flask Backend:  http://localhost:$FLASK_PORT"
echo "                http://$LOCAL_IP:$FLASK_PORT"
echo "Log file: $logfile_backend"
echo "---------------------------------------------"
