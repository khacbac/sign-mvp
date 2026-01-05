"""
Video Loader for WLASL Dataset

Downloads and caches videos from WLASL dataset on-demand.
Supports direct HTTP downloads and YouTube videos.
"""

import logging
import requests
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from urllib.parse import urlparse
import time

from .config import (
    VIDEO_CACHE_DIR,
    MAX_RETRIES,
    TIMEOUT_SECONDS,
    CHUNK_SIZE,
    MAX_CACHE_SIZE_GB,
)

# Try to import yt-dlp (may not be installed)
try:
    import yt_dlp
    _YT_DLP_AVAILABLE = True
except ImportError:
    yt_dlp = None
    _YT_DLP_AVAILABLE = False
    print("Warning: yt-dlp not available. YouTube videos cannot be downloaded.")

logger = logging.getLogger(__name__)


class VideoLoader:
    """Handles downloading and caching of WLASL videos"""

    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize video loader.

        Args:
            cache_dir: Directory to store cached videos
        """
        self.cache_dir = cache_dir or VIDEO_CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_path(self, video_id: str) -> Path:
        """Get the local cache path for a video"""
        return self.cache_dir / f"{video_id}.mp4"

    def is_cached(self, video_id: str) -> bool:
        """Check if a video is already cached locally"""
        cache_path = self._get_cache_path(video_id)
        return cache_path.exists()

    def get_local_path(self, video_id: str) -> Optional[Path]:
        """
        Get the local path to a video if it exists.

        Args:
            video_id: The video ID

        Returns:
            Path to cached video or None if not cached
        """
        cache_path = self._get_cache_path(video_id)
        return cache_path if cache_path.exists() else None

    def _get_cache_size_gb(self) -> float:
        """Get current cache size in GB"""
        total_size = 0
        for file_path in self.cache_dir.glob("*.mp4"):
            total_size += file_path.stat().st_size
        return total_size / (1024 ** 3)  # Convert bytes to GB

    def _cleanup_cache(self, target_size_gb: float):
        """
        Cleanup cache to maintain size limit.

        Args:
            target_size_gb: Target cache size in GB
        """
        cache_files = []
        for file_path in self.cache_dir.glob("*.mp4"):
            stat = file_path.stat()
            cache_files.append((file_path, stat.st_mtime, stat.st_size))

        # Sort by modification time (oldest first)
        cache_files.sort(key=lambda x: x[1])

        current_size = sum(f[2] for f in cache_files) / (1024 ** 3)

        # Remove oldest files until under target size
        for file_path, _, file_size in cache_files:
            if current_size <= target_size_gb:
                break

            try:
                file_path.unlink()
                current_size -= file_size / (1024 ** 3)
                logger.info(f"Removed cached video: {file_path.name}")
            except Exception as e:
                logger.error(f"Failed to remove {file_path}: {e}")

    def download_video(self, video_url: str, video_id: str) -> Optional[Path]:
        """
        Download a video from URL and cache it locally.
        Supports both direct HTTP downloads and YouTube videos.

        Args:
            video_url: URL to download video from (HTTP or YouTube)
            video_id: Unique video ID for caching

        Returns:
            Path to cached video or None if download failed
        """
        cache_path = self._get_cache_path(video_id)

        # Check if already cached
        if cache_path.exists():
            logger.debug(f"Video {video_id} already cached: {cache_path}")
            return cache_path

        # Check cache size before downloading
        try:
            if self._get_cache_size_gb() >= MAX_CACHE_SIZE_GB * 0.9:
                logger.info("Cache size approaching limit, cleaning up...")
                self._cleanup_cache(MAX_CACHE_SIZE_GB * 0.7)
        except Exception as e:
            logger.warning(f"Cache cleanup failed: {e}")

        # Download the video
        logger.info(f"Downloading video {video_id} from {video_url}")

        # Check if this is a YouTube URL
        if self._is_youtube_url(video_url):
            return self._download_youtube_video(video_url, video_id, cache_path)
        else:
            return self._download_http_video(video_url, video_id, cache_path)

    def _is_youtube_url(self, url: str) -> bool:
        """Check if a URL is a YouTube video URL"""
        parsed = urlparse(url)
        return (
            parsed.netloc.lower().endswith('youtube.com') or
            parsed.netloc.lower().endswith('youtu.be')
        )

    def _download_youtube_video(self, video_url: str, video_id: str, cache_path: Path) -> Optional[Path]:
        """Download a YouTube video using yt-dlp"""
        if not _YT_DLP_AVAILABLE:
            logger.error("yt-dlp not available. Cannot download YouTube videos.")
            return None

        for attempt in range(MAX_RETRIES):
            try:
                # Configure yt-dlp options
                ydl_opts = {
                    'format': 'best[ext=mp4]/best',  # Prefer mp4, otherwise best format
                    'outtmpl': str(cache_path.with_suffix('').with_suffix('')),
                    'quiet': True,
                    'no-warnings': True,
                    'noprogress': True,
                    'cookiefile': None,  # Could add cookies for age-restricted videos
                }

                # Download video
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    logger.debug(f"Downloading YouTube video {video_id}")
                    result = ydl.download([video_url])

                    if result == 0:  # Success
                        logger.info(f"Successfully downloaded YouTube video {video_id}")
                        return cache_path
                    else:
                        logger.error(f"yt-dlp download failed with code {result}")

            except Exception as e:
                logger.warning(f"YouTube download attempt {attempt + 1} failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to download YouTube video {video_id} after {MAX_RETRIES} attempts")

        return None

    def _download_http_video(self, video_url: str, video_id: str, cache_path: Path) -> Optional[Path]:
        """Download video via HTTP using requests"""
        for attempt in range(MAX_RETRIES):
            try:
                # Send GET request with streaming
                response = requests.get(
                    video_url,
                    stream=True,
                    timeout=TIMEOUT_SECONDS,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                )
                response.raise_for_status()

                # Check content type
                content_type = response.headers.get('content-type', '')
                if 'video' not in content_type and 'application/octet-stream' not in content_type:
                    logger.warning(f"Unexpected content type: {content_type}")

                # Download with progress
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0

                with open(cache_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)

                # Verify download
                if total_size > 0 and downloaded < total_size:
                    logger.error(f"Incomplete download: {downloaded}/{total_size} bytes")
                    cache_path.unlink()
                    continue

                logger.info(f"Successfully downloaded video {video_id} ({downloaded} bytes)")
                return cache_path

            except requests.exceptions.RequestException as e:
                logger.warning(f"HTTP download attempt {attempt + 1} failed: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Failed to download video {video_id} after {MAX_RETRIES} attempts")

        return None

    def get_video(self, video_url: str, video_id: str, force_refresh: bool = False) -> Optional[Path]:
        """
        Get a video, downloading it if necessary.

        Args:
            video_url: URL to download from
            video_id: Unique video ID
            force_refresh: Force re-download even if cached

        Returns:
            Path to video file or None if unavailable
        """
        if not force_refresh and self.is_cached(video_id):
            return self.get_local_path(video_id)

        return self.download_video(video_url, video_id)

    def clear_cache(self):
        """Clear all cached videos"""
        try:
            shutil.rmtree(self.cache_dir)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Cleared all cached videos")
        except Exception as e:
            logger.error(f"Failed to clear cache: {e}")

    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get information about the cache.

        Returns:
            Dictionary with cache statistics
        """
        video_files = list(self.cache_dir.glob("*.mp4"))
        total_size = sum(f.stat().st_size for f in video_files)

        return {
            "video_count": len(video_files),
            "total_size_mb": total_size / (1024 * 1024),
            "total_size_gb": total_size / (1024 ** 3),
            "cache_dir": str(self.cache_dir),
            "max_size_gb": MAX_CACHE_SIZE_GB
        }


def create_video_loader(cache_dir: Optional[Path] = None) -> VideoLoader:
    """Factory function to create video loader"""
    return VideoLoader(cache_dir)


__all__ = ["VideoLoader", "create_video_loader"]
