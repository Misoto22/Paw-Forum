#!/bin/bash

# Log file
LOG_FILE="run.log"

# Initialize log file
echo "---- Starting Script at $(date) ----" > $LOG_FILE

# Check if Python3 is installed
if ! command -v python3 &>/dev/null; then
    echo "$(date): Python3 is not installed." >> $LOG_FILE
    exit 1
else
    echo "$(date): Python3 is installed." >> $LOG_FILE
fi

# Check if Flask is installed globally (optional)
if ! python3 -c "import flask" &>/dev/null; then
    echo "$(date): Flask is not installed. Attempting to install Flask..." >> $LOG_FILE
    python3 -m pip install Flask && echo "$(date): Flask successfully installed." >> $LOG_FILE || {
        echo "$(date): Failed to install Flask." >> $LOG_FILE
        exit 1
    }
else
    echo "$(date): Flask is already installed." >> $LOG_FILE
fi

# # cd to app directory
# cd app || {
#     echo "$(date): Failed to cd to app directory." >> $LOG_FILE
#     exit 1
# }
# echo "$(date): Changed directory to app." >> $LOG_FILE

# Check if venv exists; if not, create it
if [ ! -d "venv" ]; then
    echo "$(date): Creating virtual environment..." >> $LOG_FILE
    python3 -m venv venv && echo "$(date): venv created successfully." >> $LOG_FILE || {
        echo "$(date): Failed to create venv." >> $LOG_FILE
        exit 1
    }
else
    echo "$(date): venv already exists." >> $LOG_FILE
fi

# Activate virtual environment
echo "$(date): Activating virtual environment..." >> $LOG_FILE
source venv/bin/activate && echo "$(date): venv activated." >> $LOG_FILE || {
    echo "$(date): Failed to activate venv." >> $LOG_FILE
    exit 1
}

# Set FLASK_APP environment variable
export FLASK_APP="run:create_app"

# Check if requirements.txt exists
if [ ! -f "app/requirements.txt" ]; then
    echo "$(date): requirements.txt not found." >> $LOG_FILE
    exit 1
else
    echo "$(date): requirements.txt found." >> $LOG_FILE
fi

# Install dependencies
echo "$(date): Installing dependencies..." >> $LOG_FILE
python3 -m pip install -r app/requirements.txt && echo "$(date): Dependencies installed successfully." >> $LOG_FILE || {
    echo "$(date): Failed to install dependencies." >> $LOG_FILE
    exit 1
}

# Check port availability
if netstat -tuln | grep -q ':5000\s'; then
    echo "$(date): Port 5000 is busy." >> $LOG_FILE
    exit 1
else
    echo "$(date): Port 5000 is available." >> $LOG_FILE
fi

# Run Flask app in the background
echo "$(date): Running Flask app..." >> $LOG_FILE
flask run &
FLASK_PID=$!
echo "$(date): Flask app started with PID $FLASK_PID." >> $LOG_FILE

# Sleep to ensure server starts
sleep 3

# Check if Flask app has started
if ! curl --output /dev/null --silent --head --fail "http://127.0.0.1:5000"; then
    echo "$(date): Flask app failed to start, stopping process." >> $LOG_FILE
    kill $FLASK_PID
    exit 1
else
    echo "$(date): Flask app is running." >> $LOG_FILE
fi

# Open URL based on OS
echo "$(date): Opening browser..." >> $LOG_FILE
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open http://127.0.0.1:5000
elif [[ "$OSTYPE" == "darwin"* ]]; then
    open http://127.0.0.1:5000
elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    start http://127.0.0.1:5000
else
    echo "$(date): OS not supported" >> $LOG_FILE
    exit 1
fi

# Use trap to capture INT (Ctrl-C) signals and shut down Flask gracefully
trap "echo '$(date): Stopping Flask app...'; kill $FLASK_PID; echo '$(date): Flask app stopped.' >> $LOG_FILE" INT
wait $FLASK_PID

echo "---- Script Ended at $(date) ----" >> $LOG_FILE
