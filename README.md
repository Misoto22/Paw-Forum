<div align="center">

<h1 align="center">Paw Forum (Your Lively Pet Community)</h1>

</div>

Welcome to the **Paw Forum**, the premier online destination for pet lovers and pet onwers! This web application is designed to foster a vibrant community where users can share their beloved pets, discuss various pet-related topics, and access a wealth of information on pet adoption. Whether you're looking to show off your furry friend, seek advice, or find a new family member through adoption, Paw Forum is your go-to hub for all things pets.

## Features

- **Community Discussions**: Engage in daily discussions on a wide range of pet-related topics.
- **Pet Sitting Information**: Post and browse Pet sitting informations, helping pets taken good care of when owners away.
- **Pet Adoption Information**: Post and browse adoption informations, helping pets find loving homes.
- **Interactive Posts**: Share updates, ask questions, and interact with fellow pet owners.

Paw Forum aims to connect pet enthusiasts, provide valuable information, and help ensure that every pet finds a loving home. Join us today and be a part of our growing community!

## Group Members

<div align="center">

| Student ID | Name         | Github Username |
| ---------- | ------------ | --------------- |
| 23843181   | Bella Bao    | bellabaohaha    |
| 23929804   | Xinwei Chen  | Misoto22        |
| 21938264   | Xudong Ying  | sheldonyxd      |
| 23737625   | Siting Xiang | elefantat       |

</div>


## Architecture

### File Structure

```bash
app
├── README.md                       # Project description and instructions.
├── app
│   ├── __init__.py                 # Initialize the Flask app.
│   ├── config.py                   # Configuration settings.
│   ├── app.db                      # SQLite database file.
│   ├── models.py                   # Database models.
│   ├── requirements.txt            # Dependencies.
│   ├── routes.py                   # Application routes.
│   ├── static                      # Static files.
│   │   ├── css
│   │   │   ├── profile.css         # Profile-specific styles.
│   │   │   └── style.css           # Main CSS file.
│   │   ├── image                   # Image files directory.
│   │   │   ├── avatars             # User avatar library.
│   │   │   └── uploads             # Post images.
│   │   └── js
│   │       ├── script.js           # Main JavaScript file.
│   │       └── topic_reply.js      # Topic reply functionality.
│   │       └── user_info_popup.js  # Task User Information pop up functionality.
│   └── templates                   # HTML templates.
│       ├── Profile.html            # User profile page.
│       ├── base.html               # Base template.
│       ├── components              # UI components.
│       │   ├── footer.html         # Footer component.
│       │   ├── nav_logged_in.html  # Navigation bar for logged-in users.
│       │   ├── nav_logged_out.html # Navigation bar for logged-out users.
│       │   └── post_reply.html     # Post task form.
│       │   └── reply.html          # Post reply form.
│       ├── index.html              # Homepage.
│       ├── login.html              # Login page.
│       ├── post_create.html        # Create uploads page.
│       ├── post_detail.html        # Post content page.
│       ├── reply.html              # Reply page.
│       ├── search_results.html     # Search results page.
│       ├── signup.html             # Signup page.
│       ├── users.html              # Users list page.
│       ├── notification.html       # Users notification history page.
│       ├── activity.html           # Users activity history page.
│       └── error_pages             # Error pages.
│           ├── 404.html            # 404 error page.
│           └── 500.html            # 500 error page.
├── deliverables
│   └── v1.0.mov                    # Deliverable v1.0 - User signup and login demo.
│   └── v2.0.mov                    # Deliverable v2.0 - Post create demo.
│   └── v3.0.mov                    # Deliverable v3.0 - Reply, task, search, notification and history demo.
├── run.py                          # Script to run the application.
├── run.sh                          # Shell script to run the application.
└── tests                           # Directory for test cases.
    ├── __init__.py                 # Initialize the Testing.
    ├── test_routes.py              # Unit Test cases.  
    └── test_models.py              # Unit Test cases.    
```

### Database Design

## Instructions for Running the Application

Simply run the following command in the terminal:

```bash
./run.sh
```

### Flags

- `-p` or `--port`: Define the port number. Example usage: `./run.sh -p 8080`
- `-d` or `--development`: Enable development mode. Example usage: `./run.sh -d`



The `run.sh` script automates the setup and execution of a Flask web application. Here are the detailed steps it performs:

1. **Initialize Log File:** Starts by initializing the `run.log` file to log the script operations.
2. **Argument Parsing:** Parses command-line arguments to set the port number (`-p` or `--port`) and enable development mode (`-d` or `--development`). If no port is specified, it defaults to `5000`.
3. **Check Python Installation:** Verifies if Python3 is installed on the system.
4. **Check Flask Installation:** Checks if Flask is installed globally and, if absent, attempts to install it.
5. **Virtual Environment Management:** If a virtual environment (`venv`) does not exist, it creates one using Python3.
6. **Activate Virtual Environment:** Activates the virtual environment. Logs an error and exits if activation fails.
7. **Set Flask Environment Variables:** Sets the `FLASK_APP` variable. If development mode is enabled, it also sets `FLASK_ENV` to `development` and `FLASK_DEBUG` to `1`.
8. **Dependency Installation:** Ensures a `requirements.txt` file is present and installs all dependencies listed.
9. **Check Port Availability:** Checks if the specified port is available. Logs an error and exits if the port is occupied.
10. **Run Flask Application:** Starts the Flask application in the background with the specified port and captures the process ID.
11. **Open Web Application in Browser:** Automatically opens the web application in the default web browser based on the operating system.
12. **Graceful Shutdown:** Implements a trap to capture `INT` (Ctrl-C) signals, allowing for the graceful shutdown of the Flask application.
13. **Logging:** Logs all operations to `run.log`, with critical errors causing the script to terminate and log an error message.

This script is designed to ensure a seamless setup and launch process for the Flask application, managing dependencies, environment setup, and server operation in a streamlined manner.


### Shutdown the Application

```bash
Ctrl + C
```

## Instructions for Running the Tests

Simply run:
```bash
python -m unittest discover tests
```

## Documentation

Documentation for the project can be found in the [Github Wiki](https://github.com/Misoto22/CITS5505-Group-Project/wiki). The documentation is divided into the following sections:

1. Meeting Logs
2. Frequently Asked Questions (FAQ)
