#!/bin/bash

# YouTube Scraper Installation Script

echo "========================================="
echo "YouTube Scraper Installation"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Check pip
echo ""
echo "Checking pip..."
python3 -m pip --version

if [ $? -ne 0 ]; then
    echo "Error: pip is not installed."
    echo "Please install pip first."
    exit 1
fi

# Install dependencies
echo ""
echo "Installing Python dependencies..."
python3 -m pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies."
    exit 1
fi

# Check FFmpeg
echo ""
echo "Checking for FFmpeg..."
ffmpeg -version > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "Warning: FFmpeg is not installed."
    echo "FFmpeg is optional but recommended for format conversion."
    echo ""
    echo "To install FFmpeg:"
    echo "  - Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  - macOS: brew install ffmpeg"
    echo "  - Windows: Download from https://ffmpeg.org"
else
    echo "FFmpeg is installed."
fi

# Make the script executable
echo ""
echo "Making youtube_scraper.py executable..."
chmod +x youtube_scraper.py

echo ""
echo "========================================="
echo "Installation Complete!"
echo "========================================="
echo ""
echo "Usage:"
echo "  python3 youtube_scraper.py <channel_url>"
echo ""
echo "For help:"
echo "  python3 youtube_scraper.py --help"
echo ""
