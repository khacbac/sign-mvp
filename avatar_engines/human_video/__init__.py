"""
Human Video Avatar Engine for WLASL

This module implements video-based sign language translation using the WLASL dataset.
"""

from .gloss_mapper import (
    GlossMapper,
    get_gloss_mapper,
    get_video_ids,
    get_best_video,
    gloss_exists
)
from .video_loader import VideoLoader, create_video_loader
from .config import VIDEO_CACHE_DIR

# Try to import video compositor, but handle if moviepy is not installed
try:
    from .video_compositor import VideoCompositor, create_compositor
    _compositor_available = True
except ImportError:
    print("Warning: moviepy not found. Video composition features will be limited.")
    print("Install with: pip install moviepy")
    VideoCompositor = None
    create_compositor = None
    _compositor_available = False

__all__ = [
    "GlossMapper",
    "get_gloss_mapper",
    "get_video_ids",
    "get_best_video",
    "gloss_exists",
    "VideoLoader",
    "create_video_loader",
    "VIDEO_CACHE_DIR"
]

# Add compositor to __all__ if available
if _compositor_available:
    __all__.extend(["VideoCompositor", "create_compositor"])

__version__ = "0.1.0"
