"""
Video Compositor for WLASL

Composites multiple sign videos into a single seamless video.
"""

import logging
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

# Handle both moviepy 1.x and 2.x
import moviepy
MOVIE_PY_VERSION = getattr(moviepy, '__version__', '1.0.0')

try:
    # Try moviepy 2.x imports first
    from moviepy import VideoFileClip, concatenate_videoclips
except ImportError:
    # Fall back to moviepy 1.x imports
    from moviepy.editor import VideoFileClip, concatenate_videoclips
    from moviepy.video.fx import fadein, fadeout

from .config import (
    OUTPUT_VIDEO_WIDTH,
    OUTPUT_VIDEO_HEIGHT,
    OUTPUT_FPS,
    TRANSITION_DURATION,
    TEMP_DIR
)

logger = logging.getLogger(__name__)


class VideoCompositor:
    """Composites multiple sign videos into a single video"""

    def __init__(
        self,
        output_width: int = OUTPUT_VIDEO_WIDTH,
        output_height: int = OUTPUT_VIDEO_HEIGHT,
        output_fps: int = OUTPUT_FPS,
        transition_duration: float = TRANSITION_DURATION
    ):
        """
        Initialize video compositor.

        Args:
            output_width: Output video width
            output_height: Output video height
            output_fps: Output video framerate
            transition_duration: Duration of transition between videos
        """
        self.output_width = output_width
        self.output_height = output_height
        self.output_fps = output_fps
        self.transition_duration = transition_duration

        # Ensure temp directory exists
        TEMP_DIR.mkdir(parents=True, exist_ok=True)

    def _load_video_clip(self, video_path: Path) -> Optional[VideoFileClip]:
        """
        Load a single video clip, handling various formats.

        Args:
            video_path: Path to video file

        Returns:
            VideoFileClip or None if loading failed
        """
        try:
            if not video_path.exists():
                logger.error(f"Video file does not exist: {video_path}")
                return None

            logger.debug(f"Loading video clip: {video_path} (size: {video_path.stat().st_size} bytes)")

            clip = VideoFileClip(str(video_path))

            # Log video properties
            logger.debug(f"Video loaded: {clip.size}, {clip.fps:.2f}fps, {clip.duration:.2f}s")

            # Resize if necessary (handle both MoviePy 1.x and 2.x)
            if clip.size != (self.output_width, self.output_height):
                logger.debug(f"Resizing video from {clip.size} to {(self.output_width, self.output_height)}")
                try:
                    # MoviePy 2.x
                    clip = clip.resized((self.output_width, self.output_height))
                except AttributeError:
                    # MoviePy 1.x
                    clip = clip.resize((self.output_width, self.output_height))

            # Set FPS if necessary (handle both MoviePy 1.x and 2.x)
            if clip.fps != self.output_fps:
                logger.debug(f"Setting FPS from {clip.fps} to {self.output_fps}")
                try:
                    # MoviePy 2.x
                    clip = clip.with_fps(self.output_fps)
                except AttributeError:
                    # MoviePy 1.x
                    clip = clip.set_fps(self.output_fps)

            return clip

        except Exception as e:
            logger.error(f"Failed to load video {video_path}: {e}")
            import traceback
            logger.error(f"Load error traceback:\n{traceback.format_exc()}")
            return None

    def _create_transition(self, clip1: VideoFileClip, clip2: VideoFileClip) -> VideoFileClip:
        """
        Create a transition between two clips.

        Args:
            clip1: First video clip
            clip2: Second video clip

        Returns:
            Transition clip
        """
        # Simple crossfade for now
        # clip1_fade = clip1.crossfadeout(self.transition_duration)
        # clip2_fade = clip2.crossfadein(self.transition_duration)

        # Just return clip2 for now - transitions can be added later
        return clip2

    def composite_videos(
        self,
        video_paths: List[Path],
        glosses: Optional[List[str]] = None,
        output_path: Optional[Path] = None,
        add_transitions: bool = False
    ) -> Optional[Path]:
        """
        Composite multiple videos into a single video.

        Args:
            video_paths: List of paths to video files
            glosses: List of glosses corresponding to videos (for metadata)
            output_path: Output path for final video. If None, creates temp file
            add_transitions: Whether to add transitions between videos

        Returns:
            Path to output video or None if composition failed
        """
        if not video_paths:
            logger.error("No video paths provided")
            return None

        if len(video_paths) == 1:
            logger.info("Only one video provided, returning original")
            return video_paths[0]

        # Load video clips
        clips = []
        valid_glosses = []

        for i, video_path in enumerate(video_paths):
            if not video_path.exists():
                logger.warning(f"Video not found: {video_path}")
                continue

            clip = self._load_video_clip(video_path)
            if clip is None:
                continue

            clips.append(clip)
            if glosses and i < len(glosses):
                valid_glosses.append(glosses[i])

        if not clips:
            logger.error("No valid videos could be loaded")
            return None

        try:
            logger.info(f"Compositing {len(clips)} videos")
            logger.info(f"Video settings: {self.output_width}x{self.output_height} @ {self.output_fps}fps")
            logger.info(f"Temp directory: {TEMP_DIR} (exists: {TEMP_DIR.exists()})")
            logger.info(f"Using moviepy version: {MOVIE_PY_VERSION}")

            # Create final video
            if add_transitions:
                # Add transitions between clips (implementation pending)
                final_clip = concatenate_videoclips(clips, method="compose")
            else:
                # Simple concatenate (fast)
                final_clip = concatenate_videoclips(clips, method="chain")

            # Set output path
            if output_path is None:
                # Create temporary file
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                # Use glosses in filename if available
                if valid_glosses:
                    gloss_str = "_".join(valid_glosses[:5])  # First 5 glosses
                    gloss_str = gloss_str.replace(" ", "_")[:50]  # Limit length
                    output_path = TEMP_DIR / f"wlasl_{gloss_str}_{timestamp}.mp4"
                else:
                    output_path = TEMP_DIR / f"wlasl_composite_{timestamp}.mp4"
            else:
                # Ensure output directory exists
                output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write final video
            logger.info(f"Writing composite video to {output_path}")

            final_clip.write_videofile(
                str(output_path),
                fps=self.output_fps,
                codec="libx264",
                audio=False,  # Sign videos typically don't have audio
                threads=4,
                preset="medium",  # Balance between speed and quality
                logger=None  # Suppress moviepy logging
            )

            # Clean up clips
            for clip in clips:
                clip.close()

            final_clip.close()

            logger.info(f"Successfully created composite video: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to composite videos: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Video paths: {[str(p) for p in video_paths]}")
            logger.error(f"Number of clips loaded: {len(clips)}")
            logger.error(f"Temp dir exists: {TEMP_DIR.exists()}")
            logger.error(f"Output path: {output_path if output_path else 'None'}")

            # Import traceback for full error details
            import traceback
            logger.error(f"Full traceback:\n{traceback.format_exc()}")

            return None

    def generate_output_filename(self, gloss_sequence: List[str]) -> Path:
        """
        Generate an output filename for a gloss sequence.

        Args:
            gloss_sequence: List of glosses

        Returns:
            Path for output video
        """
        if not gloss_sequence:
            gloss_str = "empty_sequence"
        else:
            # Join first few glosses, limit length
            gloss_str = "_".join(gloss_sequence[:5])
            gloss_str = gloss_str.replace(" ", "_").replace("-", "_")
            gloss_str = gloss_str[:50]  # Limit filename length

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sign_language_{gloss_str}_{timestamp}.mp4"

        return TEMP_DIR / filename

    def get_composite_info(self, video_paths: List[Path]) -> Dict[str, Any]:
        """
        Get information about videos to be composited.

        Args:
            video_paths: List of video paths

        Returns:
            Dictionary with statistics
        """
        total_duration = 0
        valid_videos = 0

        for video_path in video_paths:
            try:
                clip = VideoFileClip(str(video_path))
                total_duration += clip.duration
                valid_videos += 1
                clip.close()
            except Exception:
                continue

        return {
            "video_count": len(video_paths),
            "valid_videos": valid_videos,
            "total_duration_seconds": total_duration,
            "estimated_output_duration": total_duration + (valid_videos - 1) * self.transition_duration if valid_videos > 0 else 0,
            "transition_count": max(0, valid_videos - 1),
            "transition_duration": self.transition_duration
        }


def create_compositor(**kwargs) -> VideoCompositor:
    """Factory function to create video compositor"""
    return VideoCompositor(**kwargs)


__all__ = ["VideoCompositor", "create_compositor"]
























































