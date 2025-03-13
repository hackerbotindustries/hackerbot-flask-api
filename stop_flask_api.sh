#!/bin/bash

# Ports for Flask and React
FLASK_PORT=5000

# TODO: Change this to your actual serial port
SERIAL_PORT="/dev/ttyACM0"

echo "---------------------------------------------"
echo "STOPPING HACKERBOT FLASK API"
echo "---------------------------------------------"

# Find and kill Flask process
FLASK_PID=$(lsof -ti :$FLASK_PORT)
if [ -n "$FLASK_PID" ]; then
    echo "Stopping Flask backend (PID: $FLASK_PID)..."
    kill -2 "$FLASK_PID"  # Send SIGINT (Ctrl+C)
    sleep 2  # Give some time for graceful shutdown
    if ps -p "$FLASK_PID" > /dev/null; then
        echo "Force killing Flask backend..."
        kill -9 "$FLASK_PID"
    fi
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
