#!/bin/bash
# xdfgui launcher script
# Place this in ~/Applications/ and make it executable: chmod +x ~/Applications/xdfgui.command

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the xdfgui project directory
# Adjust this path if xdfgui is installed elsewhere
cd ~/code/xdfgui || exit 1

# Run xdfgui using uv
uv run xdfgui
