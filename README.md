# CITS5505-Group-Project

## Description

## Group Members

| Student ID | Name         | Github Username |
| ---------- | ------------ | --------------- |
| 23843181   | Bella Bao    | bellabaohaha    |
| 23929804   | Xinwei Chen  | Misoto22        |
| 21938264   | Xudong Ying  | sheldonyxd      |
| 23737625   | Siting Xiang | elefantat       |

## Architecture

### File Structure

```bash
app
├── app.py                  # Main Python file for the Flask application.
├── requirements.txt        # File containing all the dependencies.
├── database                # Directory for database-related files.
│   └── app.db              # SQLite database file.
├── static                  # Directory for static files.
│   ├── css                 # Subdirectory for CSS files.
│   │   └── style.css       # Main CSS file.
│   └── js                  # Subdirectory for JavaScript files.
│       └── script.js       # Main JavaScript file.
└── templates               # Directory for HTML templates which are rendered by Flask.
    ├── components          # UI components.
    │   └── nav-unlog.html  # Navigation bar for users who are not logged in.
    └── index.html          
```

### Database Design

## Instructions for Running the Application

Simply run the following command in the terminal:

```bash
./run.sh
```

The `run.sh` script automates the setup and execution of a Flask web application. Here are the detailed steps it performs:

1. **Check Python Installation:** Verifies if Python3 is installed on the system.
2. **Check Flask Installation:** Checks if Flask is installed globally and, if absent, attempts to install it.
3. **Navigate to App Directory:** Changes the working directory to the application's root directory (`app`). Exits with an error if the directory change fails.
4. **Virtual Environment Management:** If a virtual environment (`venv`) does not exist, it creates one using Python3.
5. **Activate Virtual Environment:** Activates the virtual environment. Logs an error and exits if activation fails.
6. **Dependency Installation:** Ensures a `requirements.txt` file is present and installs all dependencies listed.
7. **Check Port Availability:** Checks if port 5000 is available. Logs an error and exits if the port is occupied.
8. **Run Flask Application:** Starts the Flask application in the background and captures the process ID.
9. **Open Web Application in Browser:** Automatically opens the web application in the default web browser based on the operating system.
10. **Graceful Shutdown:** Implements a trap to capture `INT` (Ctrl-C) signals, allowing for the graceful shutdown of the Flask application.
11. **Logging:** Logs all operations to `run.log`, with critical errors causing the script to terminate and log an error message.

This script is designed to ensure a seamless setup and launch process for the Flask application, managing dependencies, environment setup, and server operation in a streamlined manner.


### Shutdown the Application

```bash
Ctrl + C
```

## Instructions for Running the Tests
