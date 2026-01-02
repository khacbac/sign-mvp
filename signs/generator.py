import logging
from signs.loader import gesture_exists
from signs.interpolator import interpolate_gesture, default_pose

# Set up logging
logger = logging.getLogger(__name__)

def idle(frame, total):
    """Default idle pose - returns base pose for all frames"""
    return default_pose.copy()

def generate_keypoints(gloss, frames=30):
    """
    Generate keypoint sequence for a gesture.

    Tries JSON gesture first, then falls back to IDLE pose if gesture not found.
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
        # No gesture found - use IDLE
        logger.warning(f"No gesture for '{gloss}', using IDLE")
        for f in range(frames):
            pose = idle(f, frames)
            sequence.append(pose)

    return sequence
