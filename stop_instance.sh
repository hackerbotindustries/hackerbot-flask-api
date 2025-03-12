#!/bin/bash

# Ports for Flask and React
FLASK_PORT=5000
REACT_PORT=5173

echo "#############################################"
echo "STOPPING HACKERBOT WEB APPLICATION"
echo "#############################################"

# Find and kill Flask process
FLASK_PID=$(lsof -ti :$FLASK_PORT)
if [ -n "$FLASK_PID" ]; then
    echo "Stopping Flask backend (PID: $FLASK_PID)..."
    kill "$FLASK_PID"
    echo "Flask backend stopped."
else
    echo "Flask backend not running."
fi

# Find and kill React process
REACT_PID=$(lsof -ti :$REACT_PORT)
if [ -n "$REACT_PID" ]; then
    echo "Stopping React frontend (PID: $REACT_PID)..."
    kill "$REACT_PID"
    echo "React frontend stopped."
else
    echo "React frontend not running."
fi

echo "#############################################"
echo "HACKERBOT WEB APPLICATION STOPPED"
echo "#############################################"
