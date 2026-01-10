import logging
from .loader import gesture_exists
from .interpolator import interpolate_gesture, default_pose

# Set up logging
logger = logging.getLogger(__name__)


def idle(_frame=0, _total=0):
    """
    Default idle pose - returns base pose for all frames.

    Args:
        _frame: Frame number (unused, kept for API compatibility)
        _total: Total frames (unused, kept for API compatibility)

    Returns:
        dict: Copy of default pose
    """
    return default_pose.copy()


def generate_keypoints(gloss, frames=30, use_fallback=True):
    """
    Generate keypoint sequence for a gesture.

    Tries JSON gesture first, then uses fallback strategies:
    1. Try fingerspell placeholder for short words (1-3 chars)
    2. Use unknown placeholder for longer words
    3. Fall back to IDLE pose as last resort

    Args:
        gloss (str): The gesture name to generate
        frames (int): Number of frames to generate
        use_fallback (bool): Whether to use fallback gestures for unknown words

    Returns:
        list: Sequence of pose dictionaries
    """
    sequence = []

    # Try new JSON format first
    if gesture_exists(gloss):
        logger.info(f"Using JSON gesture: {gloss}")
        for f in range(frames):
            pose = interpolate_gesture(gloss, f, frames)
            if pose is None:
                logger.warning(f"Failed to interpolate pose for {gloss}, using IDLE")
                pose = idle(f, frames)
            sequence.append(pose)
    else:
        # No gesture found - use fallback strategies
        if use_fallback:
            # Choose fallback based on word characteristics
            if len(gloss) <= 3:
                # Short words might be fingerspelled
                fallback_gloss = "FINGERSPELL"
                logger.info(
                    f"No gesture for '{gloss}' (short word), using FINGERSPELL placeholder"
                )
            else:
                # Longer unknown words
                fallback_gloss = "UNKNOWN"
                logger.info(f"No gesture for '{gloss}', using UNKNOWN placeholder")

            # Try to use fallback gesture
            if gesture_exists(fallback_gloss):
                for f in range(frames):
                    pose = interpolate_gesture(fallback_gloss, f, frames)
                    if pose is None:
                        pose = idle(f, frames)
                    sequence.append(pose)
            else:
                # Fallback gestures not available, use IDLE
                logger.warning(
                    f"Fallback gesture '{fallback_gloss}' not found, using IDLE"
                )
                for f in range(frames):
                    pose = idle(f, frames)
                    sequence.append(pose)
        else:
            # Fallback disabled - use IDLE
            logger.warning(f"No gesture for '{gloss}', using IDLE")
            for f in range(frames):
                pose = idle(f, frames)
                sequence.append(pose)

    return sequence
