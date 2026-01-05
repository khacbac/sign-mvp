"""
Configuration for WLASL Human Video Avatar Engine
"""

from pathlib import Path
from typing import Final

# Dataset paths
WLASL_METADATA_PATH: Final[Path] = Path(__file__).parent / "WLASL_v0.3.json"
VIDEO_CACHE_DIR: Final[Path] = Path(__file__).parent / "cache"

# Download settings
MAX_RETRIES: Final[int] = 3
TIMEOUT_SECONDS: Final[int] = 30
CHUNK_SIZE: Final[int] = 8192  # 8KB chunks for downloads

# Video quality preferences (in order of preference)
PREFERRED_SOURCES: Final[list[str]] = [
    "signschool",    # High quality, consistent format
    "asldeafined",   # Good quality
    "valencia-asl",  # Good quality
    "startasl",      # Good quality
    "handspeak",     # Decent quality
    "signingsavvy",  # Variable quality
    "aslu",          # YouTube, variable
    "aslpro",        # Flash format, may need conversion
    "aslsignbank",   # Good but limited
    "aslbrick",      # Variable
]

# Video settings
DEFAULT_FPS: Final[int] = 25  # Most videos are 25 FPS
MIN_VIDEO_DURATION: Final[float] = 0.5  # seconds
MAX_CACHE_SIZE_GB: Final[float] = 10.0  # Maximum cache size in GB

# AWS settings (if using S3)
AWS_BUCKET_NAME: Final[str] = "wlasl-videos"  # Placeholder
AWS_REGION: Final[str] = "us-west-1"  # Placeholder

# Composite video settings
OUTPUT_VIDEO_WIDTH: Final[int] = 1280  # 720p
OUTPUT_VIDEO_HEIGHT: Final[int] = 720
OUTPUT_FPS: Final[int] = 25
TRANSITION_DURATION: Final[float] = 0.5  # seconds between signs
TEMP_DIR: Final[Path] = Path("/tmp/wlasl_construction")

# Ensure directories exist
VIDEO_CACHE_DIR.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)
