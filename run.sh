#!/bin/bash

# Log file
LOG_FILE="run.log"

initialize_log() {
    # Initialize log file
    echo "---- Starting Script at $(date) ----" > $LOG_FILE
}

parse_arguments() {
    # Default values
    PORT=5000
    DEVELOPMENT_MODE=false

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        key="$1"
        case $key in
            -p|--port)
            PORT="$2"
            shift # past argument
            shift # past value
            ;;
            -d|--development)
            DEVELOPMENT_MODE=true
            shift # past argument
            ;;
            *)
            echo "$(date): Unknown option $key" >> $LOG_FILE
            exit 1
            ;;
        esac
    done

    echo "$(date): Using port number $PORT." >> $LOG_FILE
    if $DEVELOPMENT_MODE; then
        echo "$(date): Development mode enabled." >> $LOG_FILE
    fi
}

check_python() {
    if ! command -v python3 &>/dev/null; then
        echo "$(date): Python3 is not installed." >> $LOG_FILE
        exit 1
    else
        echo "$(date): Python3 is installed." >> $LOG_FILE
    fi
}

check_flask() {
    if ! python3 -c "import flask" &>/dev/null; then
        echo "$(date): Flask is not installed. Attempting to install Flask..." >> $LOG_FILE
        python3 -m pip install Flask && echo "$(date): Flask successfully installed." >> $LOG_FILE || {
            echo "$(date): Failed to install Flask." >> $LOG_FILE
            exit 1
        }
    else
        echo "$(date): Flask is already installed." >> $LOG_FILE
    fi
}

setup_venv() {
    if [ ! -d "venv" ]; then
        echo "$(date): Creating virtual environment..." >> $LOG_FILE
        python3 -m venv venv && echo "$(date): venv created successfully." >> $LOG_FILE || {
            echo "$(date): Failed to create venv." >> $LOG_FILE
            exit 1
        }
    else
        echo "$(date): venv already exists." >> $LOG_FILE
    fi

    echo "$(date): Activating virtual environment..." >> $LOG_FILE
    source venv/bin/activate && echo "$(date): venv activated." >> $LOG_FILE || {
        echo "$(date): Failed to activate venv." >> $LOG_FILE
        exit 1
    }
}

set_flask_env() {
    export FLASK_APP="run:create_app"
    if $DEVELOPMENT_MODE; then
        export FLASK_ENV="development"
        export FLASK_DEBUG=1
    fi
}

install_dependencies() {
    if [ ! -f "app/requirements.txt" ]; then
        echo "$(date): requirements.txt not found." >> $LOG_FILE
        exit 1
    else
        echo "$(date): requirements.txt found." >> $LOG_FILE
    fi

    echo "$(date): Installing dependencies..." >> $LOG_FILE
    python3 -m pip install -r app/requirements.txt && echo "$(date): Dependencies installed successfully." >> $LOG_FILE || {
        echo "$(date): Failed to install dependencies." >> $LOG_FILE
        exit 1
    }
}

check_port_availability() {
    if netstat -tuln | grep -q ":$PORT\s"; then
        echo "$(date): Port $PORT is busy." >> $LOG_FILE
        exit 1
    else
        echo "$(date): Port $PORT is available." >> $LOG_FILE
    fi
}

run_flask_app() {
    echo "$(date): Running Flask app..." >> $LOG_FILE
    flask run --port=$PORT &
    FLASK_PID=$!
    echo "$(date): Flask app started with PID $FLASK_PID." >> $LOG_FILE

    sleep 1

    if ! curl --output /dev/null --silent --head --fail "http://127.0.0.1:$PORT"; then
        echo "$(date): Flask app failed to start, stopping process." >> $LOG_FILE
        kill $FLASK_PID
        exit 1
    else
        echo "$(date): Flask app is running." >> $LOG_FILE
    fi
}

open_browser() {
    echo "$(date): Opening browser..." >> $LOG_FILE
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        xdg-open http://127.0.0.1:$PORT
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        open http://127.0.0.1:$PORT
    elif [[ "$OSTYPE" == "cygwin" || "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        start http://127.0.0.1:$PORT
    else
        echo "$(date): OS not supported" >> $LOG_FILE
        exit 1
    fi
}

trap_cleanup() {
    echo "$(date): Stopping Flask app..."
    kill $FLASK_PID
    echo "$(date): Flask app stopped." >> $LOG_FILE
}

main() {
    initialize_log
    parse_arguments "$@"
    check_python
    check_flask
    setup_venv
    set_flask_env
    install_dependencies
    check_port_availability
    run_flask_app
    open_browser

    # Use trap to capture INT (Ctrl-C) signals and shut down Flask gracefully
    trap "trap_cleanup" INT
    wait $FLASK_PID

    echo "---- Script Ended at $(date) ----" >> $LOG_FILE
}

main "$@"
