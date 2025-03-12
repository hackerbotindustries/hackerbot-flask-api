#!/bin/bash
set -o pipefail

BASE_DIR="$(pwd)"

# Log directory setup
timestamp="hackerbot_$(date '+%Y%m%d%H%M')"
logdir="$HOME/hackerbot_web_logs"
mkdir -p "$logdir"

# Keep only the latest 5 logs
ls -1dt "$logdir"/* | tail -n +6 | xargs rm -rf 2>/dev/null

logfile_backend="$logdir/$timestamp_flask.txt"
logfile_frontend="$logdir/$timestamp_react.txt"

# Port configuration
FLASK_PORT=5000
REACT_PORT=5173

function echo_failure {
    echo ""
    echo "#############################################"
    echo "FAILURE! Hackerbot web application failed to launch."
    echo "Check logs in: $logdir"
    echo "#############################################"
    exit 1
}

echo "#############################################"
echo "STARTING HACKERBOT WEB APPLICATION"
echo "#############################################"

# Start Flask Backend
cd "$BASE_DIR/hackerbot_flask_api" || { echo "Flask app directory not found!"; echo_failure; }
(flask run --host=0.0.0.0 --port=$FLASK_PORT |& tee "$logfile_backend") &
PID_BACKEND=$!

# Start React Frontend
cd "$BASE_DIR/hackerbot_command_center" || { echo "React app directory not found!"; echo_failure; }
(npm run dev -- --host --port $REACT_PORT |& tee "$logfile_frontend") &
PID_FRONTEND=$!

# Wait a few seconds for processes to start
sleep 5

# Check if processes are running
if ! ps -p $PID_BACKEND > /dev/null; then
    echo "Flask backend failed to start!"
    echo_failure
fi

if ! ps -p $PID_FRONTEND > /dev/null; then
    echo "React frontend failed to start!"
    echo_failure
fi

echo ""
echo "#############################################"
echo "SUCCESS! Hackerbot Web Application is Running!"
echo "Flask Backend:  http://localhost:$FLASK_PORT"
echo "React Frontend: http://localhost:$REACT_PORT"
echo "#############################################"
