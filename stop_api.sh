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
# This script stops the Hackerbot Fast API process and releases the serial port.
#
# Special thanks to the following for their code contributions to this codebase:
# Allen Chien - https://github.com/AllenChienXXX
################################################################################


#!/bin/bash

# Port for FastAPI (same as in launch script)
FASTAPI_PORT=5000

echo "---------------------------------------------"
echo "STOPPING HACKERBOT FASTAPI API"
echo "---------------------------------------------"

# Try finding by port
FASTAPI_PID=$(lsof -ti :$FASTAPI_PORT)

# Fallback: search for uvicorn process
if [ -z "$FASTAPI_PID" ]; then
    FASTAPI_PID=$(pgrep -f "uvicorn")
fi

if [ -n "$FASTAPI_PID" ]; then
    echo "Stopping FastAPI backend (PID: $FASTAPI_PID)..."
    kill -2 $FASTAPI_PID
    sleep 2
    for pid in $FASTAPI_PID; do
        if ps -p "$pid" > /dev/null; then
            echo "Force killing FastAPI backend PID $pid..."
            kill -9 "$pid"
        fi
    done
    echo "FastAPI backend stopped."
else
    echo "FastAPI backend not running."
fi

echo "---------------------------------------------"
echo "CHECKING SERIAL PORTS (/dev/ttyACM*)"
echo "---------------------------------------------"

for SERIAL_PORT in /dev/ttyACM*; do
    if [ -e "$SERIAL_PORT" ]; then
        echo "Checking serial port $SERIAL_PORT..."
        if lsof "$SERIAL_PORT" &>/dev/null; then
            SERIAL_PID=$(lsof -t "$SERIAL_PORT")
            echo "Releasing serial port $SERIAL_PORT (PID: $SERIAL_PID)..."
            kill -9 "$SERIAL_PID"
            echo "Serial port $SERIAL_PORT is now free."
        else
            echo "Serial port $SERIAL_PORT is not occupied."
        fi
    fi
done

echo "---------------------------------------------"
echo "HACKERBOT FASTAPI API STOPPED"
echo "---------------------------------------------"
