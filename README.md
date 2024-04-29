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

### Shutdown the Application

```bash
Ctrl + C
```

## Instructions for Running the Tests
