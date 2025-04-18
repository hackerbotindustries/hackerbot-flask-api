#!/bin/bash
################################################################################
# Copyright (c) 2025 Hackerbot Industries LLC
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
#
# Created By: Allen Chien
# Created:    April 2025
# Updated:    2025.04.01
#
# This script stops the Hackerbot Flask API process and releases the serial port.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


# Ports for Flask and React
FLASK_PORT=5000

# TODO: Change this to your actual serial port
SERIAL_PORT="/dev/ttyACM1"

echo "---------------------------------------------"
echo "STOPPING HACKERBOT FLASK API"
echo "---------------------------------------------"

# First try finding by port (if known)
FLASK_PID=$(lsof -ti :$FLASK_PORT)

# Fallback: find flask process explicitly
if [ -z "$FLASK_PID" ]; then
    FLASK_PID=$(pgrep -f "flask run")
fi

if [ -n "$FLASK_PID" ]; then
    echo "Stopping Flask backend (PID: $FLASK_PID)..."
    kill -2 $FLASK_PID  # no quotes here!
    sleep 2  # Give it time to shut down
    for pid in $FLASK_PID; do
        if ps -p "$pid" > /dev/null; then
            echo "Force killing Flask backend PID $pid..."
            kill -9 "$pid"
        fi
    done
    echo "Flask backend stopped."
else
    echo "Flask backend not running."
fi


echo "---------------------------------------------"
echo "CHECKING SERIAL PORT $SERIAL_PORT"
echo "---------------------------------------------"

# Check if the serial port is occupied
if lsof "$SERIAL_PORT" &>/dev/null; then
    SERIAL_PID=$(lsof -t "$SERIAL_PORT")
    echo "Releasing serial port $SERIAL_PORT (PID: $SERIAL_PID)..."
    kill -9 "$SERIAL_PID"
    echo "Serial port $SERIAL_PORT is now free."
else
    echo "Serial port $SERIAL_PORT is not occupied."
fi

echo "---------------------------------------------"
echo "HACKERBOT FLASK API STOPPED"
echo "---------------------------------------------"
