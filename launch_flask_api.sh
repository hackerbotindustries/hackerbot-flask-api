#!/bin/bash
set -o pipefail

BASE_DIR="$(pwd)"

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
    echo "Check logs in: $logdir"
    echo "---------------------------------------------"
    exit 1
}

echo "---------------------------------------------"
echo "STARTING HACKERBOT FLASK API"
echo "---------------------------------------------"

# Start Flask Backend
FLASK_APP=app.py FLASK_ENV=development flask run --host=0.0.0.0 --port=$FLASK_PORT --no-debugger --no-reload >> "$logfile_backend" 2>&1 &
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
