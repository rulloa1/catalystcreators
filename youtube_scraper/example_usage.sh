#!/bin/bash

# Example Usage Script for YouTube Scraper
# This script demonstrates various ways to use the YouTube scraper

echo "YouTube Scraper - Example Usage"
echo "================================"
echo ""
echo "This script shows example commands. Edit the CHANNEL_URL variable below."
echo ""

# EDIT THIS: Set your target YouTube channel URL
CHANNEL_URL="https://www.youtube.com/@example"

echo "Example 1: Download all videos (best quality, MP4)"
echo "Command: python3 youtube_scraper.py $CHANNEL_URL"
echo ""

echo "Example 2: Download to custom directory"
echo "Command: python3 youtube_scraper.py $CHANNEL_URL -o my_downloads"
echo ""

echo "Example 3: Download only 10 videos in 720p"
echo "Command: python3 youtube_scraper.py $CHANNEL_URL -m 10 -q 720p"
echo ""

echo "Example 4: Download without metadata (saves space)"
echo "Command: python3 youtube_scraper.py $CHANNEL_URL --no-metadata"
echo ""

echo "Example 5: Download in 1080p, limit to 50 videos"
echo "Command: python3 youtube_scraper.py $CHANNEL_URL -q 1080p -m 50 -o videos_1080p"
echo ""

echo "Example 6: Download in WebM format"
echo "Command: python3 youtube_scraper.py $CHANNEL_URL -f webm"
echo ""

echo "================================"
echo "To actually run any of these examples, uncomment the desired line below:"
echo ""

# Uncomment ONE of these lines to run an example:

# Example 1: Basic download
# python3 youtube_scraper.py "$CHANNEL_URL"

# Example 2: Custom directory
# python3 youtube_scraper.py "$CHANNEL_URL" -o my_downloads

# Example 3: Limited downloads
# python3 youtube_scraper.py "$CHANNEL_URL" -m 10 -q 720p

# Example 4: No metadata
# python3 youtube_scraper.py "$CHANNEL_URL" --no-metadata

# Example 5: High quality, limited
# python3 youtube_scraper.py "$CHANNEL_URL" -q 1080p -m 50 -o videos_1080p

# Example 6: Different format
# python3 youtube_scraper.py "$CHANNEL_URL" -f webm

echo "For more options, run: python3 youtube_scraper.py --help"
