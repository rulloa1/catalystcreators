# YouTube Channel Scraper & Downloader

A powerful Python application to scrape and download all videos from any YouTube channel.

## Features

- Download all videos from a YouTube channel
- Support for multiple video qualities (best, 1080p, 720p, etc.)
- Multiple format options (MP4, WebM, MKV)
- Progress tracking with real-time updates
- Automatic resume of interrupted downloads
- Download metadata (thumbnails, descriptions, video info)
- Comprehensive logging
- Prevents re-downloading already downloaded videos
- Error handling and recovery

## Requirements

- Python 3.8 or higher
- Internet connection
- FFmpeg (optional, for format conversion)

## Installation

### 1. Clone or navigate to the repository

```bash
cd youtube_scraper
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg (Optional but Recommended)

FFmpeg is used for video format conversion and merging.

**On Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**On macOS:**
```bash
brew install ffmpeg
```

**On Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## Usage

### Basic Usage

Download all videos from a channel:

```bash
python youtube_scraper.py https://www.youtube.com/@channelname
```

### Advanced Usage

**Specify output directory:**
```bash
python youtube_scraper.py https://www.youtube.com/@channelname -o my_videos
```

**Download in specific quality:**
```bash
python youtube_scraper.py https://www.youtube.com/@channelname -q 1080p
```

**Limit number of downloads:**
```bash
python youtube_scraper.py https://www.youtube.com/@channelname -m 10
```

**Download without metadata:**
```bash
python youtube_scraper.py https://www.youtube.com/@channelname --no-metadata
```

**Combine options:**
```bash
python youtube_scraper.py https://www.youtube.com/@channelname -o downloads -q 720p -f mp4 -m 50
```

### Command Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `channel_url` | - | YouTube channel URL (required) | - |
| `--output` | `-o` | Output directory | `downloads` |
| `--quality` | `-q` | Video quality | `best` |
| `--format` | `-f` | Video format | `mp4` |
| `--max-downloads` | `-m` | Maximum videos to download | All |
| `--no-metadata` | - | Skip metadata download | False |

### Quality Options

- `best` - Best available quality
- `worst` - Lowest quality
- `2160p` - 4K quality
- `1440p` - 2K quality
- `1080p` - Full HD
- `720p` - HD
- `480p` - SD
- `360p` - Low quality

### Format Options

- `mp4` - MP4 format (recommended)
- `webm` - WebM format
- `mkv` - MKV format

## Supported URL Formats

The scraper supports various YouTube URL formats:

```bash
https://www.youtube.com/@username
https://www.youtube.com/c/channelname
https://www.youtube.com/channel/CHANNEL_ID
https://www.youtube.com/user/username
```

## Output Structure

Downloaded videos are organized as follows:

```
downloads/
├── archive.txt                  # Archive of downloaded videos
├── scraper.log                  # Log file
└── [Channel Name]/
    ├── Video 1.mp4
    ├── Video 1.info.json        # Metadata (if enabled)
    ├── Video 1.description      # Description (if enabled)
    ├── Video 1.jpg              # Thumbnail (if enabled)
    ├── Video 2.mp4
    └── ...
```

## Features in Detail

### Download Archive

The scraper maintains an `archive.txt` file that tracks all downloaded videos. This prevents re-downloading videos when you run the script again on the same channel.

### Logging

All activities are logged to:
- Console output (real-time)
- `scraper.log` file in the output directory

Logs include:
- Download progress
- Video information
- Errors and warnings
- Completion status

### Error Handling

The scraper handles errors gracefully:
- Continues downloading even if individual videos fail
- Logs errors for later review
- Supports resume of interrupted downloads

### Metadata Files

When metadata is enabled (default), the scraper downloads:
- `.info.json` - Complete video metadata (title, description, uploader, etc.)
- `.description` - Video description text
- `.jpg` - Video thumbnail image

## Examples

### Example 1: Download entire channel in best quality

```bash
python youtube_scraper.py https://www.youtube.com/@veritasium
```

### Example 2: Download 20 most recent videos in 720p

```bash
python youtube_scraper.py https://www.youtube.com/@veritasium -m 20 -q 720p
```

### Example 3: Download to external drive

```bash
python youtube_scraper.py https://www.youtube.com/@veritasium -o /mnt/external/youtube_archive
```

### Example 4: Download without metadata to save space

```bash
python youtube_scraper.py https://www.youtube.com/@veritasium --no-metadata
```

## Troubleshooting

### Issue: "yt-dlp is not installed"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Downloads are slow

**Solutions:**
- Check your internet connection
- Try a lower quality setting (-q 720p or -q 480p)
- YouTube may be rate-limiting; try again later

### Issue: Format conversion fails

**Solution:**
Install FFmpeg (see Installation section above)

### Issue: "Video unavailable" errors

**Possible causes:**
- Video is private or deleted
- Video has age restrictions
- Geographic restrictions

The scraper will log these errors and continue with other videos.

### Issue: Disk space running out

**Solutions:**
- Use `--max-downloads` to limit number of videos
- Use lower quality settings
- Use `--no-metadata` to skip metadata files
- Regularly move downloaded videos to external storage

## Performance Tips

1. **For large channels (1000+ videos):**
   - Download in batches using `--max-downloads`
   - Monitor disk space regularly
   - Consider using lower quality for archival purposes

2. **For faster downloads:**
   - Use `--no-metadata` if you don't need metadata
   - Ensure stable internet connection
   - Download during off-peak hours

3. **For bandwidth conservation:**
   - Use lower quality settings (480p or 360p)
   - Limit concurrent downloads

## Legal and Ethical Considerations

**Important:**

- Only download videos you have the right to download
- Respect copyright and terms of service
- YouTube's Terms of Service generally prohibit downloading videos
- This tool is for educational purposes and personal backups only
- Do not redistribute downloaded content
- Consider supporting creators through official channels

## License

This project is for educational and personal use only.

## Contributing

Feel free to submit issues or pull requests for improvements.

## Acknowledgments

- Built with [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Uses FFmpeg for video processing
