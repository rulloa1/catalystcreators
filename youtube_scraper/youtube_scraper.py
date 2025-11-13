#!/usr/bin/env python3
"""
YouTube Channel Scraper and Downloader

This script downloads all videos from a specified YouTube channel.
Uses yt-dlp for robust downloading with progress tracking and error handling.
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed. Please run: pip install -r requirements.txt")
    sys.exit(1)


class YouTubeScraper:
    """YouTube channel scraper and video downloader."""

    def __init__(
        self,
        channel_url: str,
        output_dir: str = "downloads",
        quality: str = "best",
        format_type: str = "mp4",
        download_metadata: bool = True,
        max_downloads: Optional[int] = None
    ):
        """
        Initialize the YouTube scraper.

        Args:
            channel_url: URL of the YouTube channel or username
            output_dir: Directory to save downloaded videos
            quality: Video quality (best, worst, or specific resolution like 1080p)
            format_type: Video format (mp4, webm, etc.)
            download_metadata: Whether to download video metadata
            max_downloads: Maximum number of videos to download (None for all)
        """
        self.channel_url = channel_url
        self.output_dir = Path(output_dir)
        self.quality = quality
        self.format_type = format_type
        self.download_metadata = download_metadata
        self.max_downloads = max_downloads

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Setup logging
        self._setup_logging()

    def _setup_logging(self):
        """Configure logging for the scraper."""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.FileHandler(self.output_dir / 'scraper.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def _get_ydl_opts(self) -> Dict[str, Any]:
        """
        Get yt-dlp options configuration.

        Returns:
            Dictionary of yt-dlp options
        """
        # Determine format based on quality and format type
        if self.quality == "best":
            format_string = f'bestvideo[ext={self.format_type}]+bestaudio[ext=m4a]/best[ext={self.format_type}]/best'
        elif self.quality == "worst":
            format_string = 'worst'
        else:
            # Specific resolution like 1080p, 720p, etc.
            format_string = f'bestvideo[height<={self.quality[:-1]}][ext={self.format_type}]+bestaudio/best'

        ydl_opts = {
            'format': format_string,
            'outtmpl': str(self.output_dir / '%(uploader)s/%(title)s.%(ext)s'),
            'ignoreerrors': True,  # Continue on download errors
            'no_warnings': False,
            'quiet': False,
            'no_color': False,
            'progress_hooks': [self._progress_hook],
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': self.format_type,
            }],
            # Download metadata files
            'writeinfojson': self.download_metadata,
            'writedescription': self.download_metadata,
            'writethumbnail': self.download_metadata,
            'writesubtitles': False,
            'writeautomaticsub': False,
            # Archive file to avoid re-downloading
            'download_archive': str(self.output_dir / 'archive.txt'),
        }

        if self.max_downloads:
            ydl_opts['playlistend'] = self.max_downloads

        return ydl_opts

    def _progress_hook(self, d: Dict[str, Any]):
        """
        Hook function for download progress updates.

        Args:
            d: Progress dictionary from yt-dlp
        """
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            self.logger.info(f"Downloading: {percent} at {speed} (ETA: {eta})")
        elif d['status'] == 'finished':
            self.logger.info(f"Finished downloading: {d.get('filename', 'unknown')}")
        elif d['status'] == 'error':
            self.logger.error(f"Error downloading: {d.get('filename', 'unknown')}")

    def get_channel_info(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve information about the YouTube channel.

        Returns:
            Dictionary containing channel information or None if error
        """
        self.logger.info(f"Fetching channel information from: {self.channel_url}")

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,  # Don't download, just extract info
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.channel_url, download=False)

                if info:
                    channel_name = info.get('uploader', info.get('channel', 'Unknown'))
                    video_count = info.get('playlist_count', len(info.get('entries', [])))

                    self.logger.info(f"Channel: {channel_name}")
                    self.logger.info(f"Total videos found: {video_count}")

                    return {
                        'channel_name': channel_name,
                        'video_count': video_count,
                        'title': info.get('title', 'Unknown'),
                        'description': info.get('description', ''),
                    }
        except Exception as e:
            self.logger.error(f"Error fetching channel info: {str(e)}")
            return None

    def download_all_videos(self):
        """Download all videos from the channel."""
        self.logger.info("="*60)
        self.logger.info("Starting YouTube Channel Download")
        self.logger.info("="*60)

        # Get channel info first
        channel_info = self.get_channel_info()
        if not channel_info:
            self.logger.error("Failed to retrieve channel information. Exiting.")
            return False

        download_limit = self.max_downloads or channel_info['video_count']
        self.logger.info(f"Will attempt to download {download_limit} videos")
        self.logger.info(f"Output directory: {self.output_dir.absolute()}")
        self.logger.info("="*60)

        # Download videos
        ydl_opts = self._get_ydl_opts()

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.logger.info("Starting downloads...")
                ydl.download([self.channel_url])
                self.logger.info("="*60)
                self.logger.info("Download process completed!")
                self.logger.info(f"Videos saved to: {self.output_dir.absolute()}")
                self.logger.info("="*60)
                return True
        except Exception as e:
            self.logger.error(f"Error during download: {str(e)}")
            return False


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Download all videos from a YouTube channel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all videos from a channel
  python youtube_scraper.py https://www.youtube.com/@channelname

  # Download with custom output directory
  python youtube_scraper.py https://www.youtube.com/@channelname -o my_videos

  # Download only 10 videos in 720p
  python youtube_scraper.py https://www.youtube.com/@channelname -m 10 -q 720p

  # Download without metadata
  python youtube_scraper.py https://www.youtube.com/@channelname --no-metadata

Supported URL formats:
  - https://www.youtube.com/@username
  - https://www.youtube.com/c/channelname
  - https://www.youtube.com/channel/CHANNEL_ID
  - https://www.youtube.com/user/username
        """
    )

    parser.add_argument(
        'channel_url',
        help='YouTube channel URL or username'
    )

    parser.add_argument(
        '-o', '--output',
        default='downloads',
        help='Output directory for downloaded videos (default: downloads)'
    )

    parser.add_argument(
        '-q', '--quality',
        default='best',
        choices=['best', 'worst', '2160p', '1440p', '1080p', '720p', '480p', '360p'],
        help='Video quality (default: best)'
    )

    parser.add_argument(
        '-f', '--format',
        default='mp4',
        choices=['mp4', 'webm', 'mkv'],
        help='Video format (default: mp4)'
    )

    parser.add_argument(
        '-m', '--max-downloads',
        type=int,
        help='Maximum number of videos to download (default: all)'
    )

    parser.add_argument(
        '--no-metadata',
        action='store_true',
        help='Do not download metadata files'
    )

    return parser.parse_args()


def main():
    """Main entry point for the script."""
    args = parse_arguments()

    # Create scraper instance
    scraper = YouTubeScraper(
        channel_url=args.channel_url,
        output_dir=args.output,
        quality=args.quality,
        format_type=args.format,
        download_metadata=not args.no_metadata,
        max_downloads=args.max_downloads
    )

    # Download all videos
    success = scraper.download_all_videos()

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
