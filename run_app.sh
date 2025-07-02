#!/bin/bash
# This script sets up the virtual environment and runs the Ekman Transport GUI application.

# Set the virtual environment directory name
VENV_DIR=".venv"

# Use python3 as the base interpreter
PYTHON_CMD="python3"

# --- Functions ---

# Function to print messages
print_message() {
    echo "--------------------------------------------------"
    echo "$1"
    echo "--------------------------------------------------"
}

# Function to handle errors
handle_error() {
    echo "Error: $1"
    exit 1
}

# --- Main Script ---

# 1. Check for python3
if ! command -v $PYTHON_CMD &> /dev/null; then
    handle_error "python3 is not installed or not in PATH. Please install Python 3.8+."
fi

# 2. Set up the virtual environment
if [ ! -d "$VENV_DIR" ]; then
    print_message "Creating virtual environment in '$VENV_DIR'..."
    $PYTHON_CMD -m venv "$VENV_DIR" || handle_error "Failed to create virtual environment."
else
    print_message "Virtual environment '$VENV_DIR' already exists."
fi

# Define python and pip executables from the virtual environment
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"

# 3. Install/update dependencies
print_message "Installing/updating dependencies from requirements.txt..."
"$VENV_PIP" install --upgrade pip > /dev/null
"$VENV_PIP" install -r requirements.txt || handle_error "Failed to install dependencies."

# 4. Run the application
print_message "Starting the Ekman Transport Visualization application..."
"$VENV_PYTHON" gui_app.py

print_message "Application has been shut down." 