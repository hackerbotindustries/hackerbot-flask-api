#!/bin/bash
################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.05.16
#
# This script launches the Hackerbot API process and occupies the serial port.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


#!/bin/bash
set -o pipefail

BASE_DIR="$(pwd)"
cd $HOME/hackerbot/hackerbot-api/

# === Log setup ===
timestamp_fastapi="hackerbot_api_$(date '+%Y%m%d%H%M')"
logdir="$HOME/hackerbot/logs"

if [ ! -d "$logdir" ]; then
    echo "Creating log directory at $logdir"
    mkdir -p "$logdir"
fi

# Keep only the latest 5 logs
ls -1dt "$logdir"/* | tail -n +6 | xargs rm -rf 2>/dev/null

logfile_backend="$logdir/$timestamp_fastapi.txt"

# === Port + IP setup ===
API_PORT=5000
LOCAL_IP=$(hostname -I | awk '{print $1}')

function echo_failure {
    echo ""
    echo "---------------------------------------------"
    echo "FAILURE! Hackerbot API failed to launch."
    echo "Check logs in: $logfile_backend"
    echo "---------------------------------------------"
    exit 1
}

echo "---------------------------------------------"
echo "STARTING HACKERBOT API"
echo "---------------------------------------------"

# === Cleanup ===
if [ -f "./stop_api.sh" ]; then
    echo "Clean up existing process..."
    if ! ./stop_api.sh >> "$logfile_backend" 2>&1; then
        echo "Warning: stop_api.sh failed during cleanup"
    fi
else
    echo "stop_api.sh not found. Skipping cleanup."
fi

# === Launch FastAPI with uvicorn ===
# Adjust `app.main:app` to your actual ASGI app import path
UVICORN_MODULE="app.main:app"  # Change if your ASGI app is elsewhere

# Production: remove --reload
uvicorn $UVICORN_MODULE \
    --host 0.0.0.0 \
    --port $API_PORT \
    --log-level info \
    --no-access-log \
    >> "$logfile_backend" 2>&1 &

PID_BACKEND=$!

# Wait for server to boot
sleep 5

if ! ps -p $PID_BACKEND > /dev/null; then
    echo "API backend failed to start!"
    echo_failure
fi

echo ""
echo "---------------------------------------------"
echo "SUCCESS! Hackerbot API Application is Running!"
echo "FastAPI Backend: http://localhost:$API_PORT"
echo "                 http://$LOCAL_IP:$API_PORT"
echo "Log file: $logfile_backend"
echo "---------------------------------------------"