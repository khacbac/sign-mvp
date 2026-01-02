"""
Keyframe Interpolator

Interpolates between gesture keyframes to generate smooth animations.
"""

from typing import Dict, List, Optional, Tuple, Any
from signs.loader import load_gesture, VALID_JOINTS
import logging

logger = logging.getLogger(__name__)

# Default pose for any undefined joints
default_pose = {
    "LEFT_SHOULDER": (0.45, 0.5),
    "LEFT_ELBOW": (0.45, 0.45),
    "LEFT_WRIST": (0.45, 0.4),
    "RIGHT_SHOULDER": (0.55, 0.5),
    "RIGHT_ELBOW": (0.55, 0.45),
    "RIGHT_WRIST": (0.55, 0.4)
}


def linear_interpolate(start: float, end: float, t: float) -> float:
    """
    Linear interpolation between two values.

    Args:
        start: Starting value
        end: Ending value
        t: Interpolation parameter (0-1)

    Returns:
        Interpolated value
    """
    return start + (end - start) * t


def find_surrounding_keyframes(keyframes: List[Dict[str, Any]], progress: float) -> Tuple[Dict, Dict, float]:
    """
    Find the keyframes surrounding a given progress position.

    Args:
        keyframes: List of keyframes sorted by time
        progress: Progress value (0-1)

    Returns:
        Tuple of (prev_keyframe, next_keyframe, interpolation_factor)
    """
    # Clamp progress to valid range
    progress = max(0.0, min(1.0, progress))

    # Handle edge cases
    if len(keyframes) == 1:
        # Only one keyframe, return it for both prev and next
        return keyframes[0], keyframes[0], 0.0

    if progress <= keyframes[0]["time"]:
        return keyframes[0], keyframes[0], 0.0

    if progress >= keyframes[-1]["time"]:
        return keyframes[-1], keyframes[-1], 0.0

    # Find surrounding keyframes
    prev_kf = keyframes[0]
    next_kf = keyframes[-1]

    for i in range(len(keyframes) - 1):
        if keyframes[i]["time"] <= progress <= keyframes[i + 1]["time"]:
            prev_kf = keyframes[i]
            next_kf = keyframes[i + 1]
            break

    # Calculate interpolation factor
    time_range = next_kf["time"] - prev_kf["time"]
    if time_range == 0:
        interpolation_factor = 0.0
    else:
        interpolation_factor = (progress - prev_kf["time"]) / time_range

    return prev_kf, next_kf, interpolation_factor


def interpolate_pose(prev_pose: Dict[str, Tuple[float, float]],
                     next_pose: Dict[str, Tuple[float, float]],
                     interpolation_factor: float) -> Dict[str, Tuple[float, float]]:
    """
    Interpolate between two poses.

    Args:
        prev_pose: Starting pose
        next_pose: Ending pose
        interpolation_factor: Interpolation factor (0-1)

    Returns:
        Interpolated pose
    """
    result_pose = {}

    # Get all unique joints from both poses
    all_joints = set(prev_pose.keys()) | set(next_pose.keys())

    for joint in all_joints:
        if joint not in VALID_JOINTS and joint not in default_pose:
            continue

        # Use default pose if joint is missing
        if joint in prev_pose:
            prev_coords = prev_pose[joint]
        else:
            prev_coords = default_pose[joint]

        if joint in next_pose:
            next_coords = next_pose[joint]
        else:
            next_coords = default_pose[joint]

        # If both poses are the same, just use that value
        if prev_coords == next_coords:
            result_pose[joint] = prev_coords
        else:
            # Interpolate x and y separately
            x = linear_interpolate(prev_coords[0], next_coords[0], interpolation_factor)
            y = linear_interpolate(prev_coords[1], next_coords[1], interpolation_factor)
            result_pose[joint] = (x, y)

    return result_pose


def interpolate_gesture(gesture_name: str, frame: int, total_frames: int) -> Optional[Dict[str, Tuple[float, float]]]:
    """
    Generate a pose for a specific frame of a gesture.

    Args:
        gesture_name: Name of the gesture
        frame: Current frame number (0-indexed)
        total_frames: Total number of frames in the animation

    Returns:
        Dict mapping joints to coordinates, or None if gesture not found
    """
    gesture = load_gesture(gesture_name)
    if not gesture:
        logger.warning(f"Gesture not found: {gesture_name}")
        return None

    # Use gesture's defined frame count or provided total_frames
    # The original generator.py uses the provided frames parameter
    gesture_frames = gesture.get("frames", total_frames)

    # Calculate progress (0-1)
    if gesture_frames <= 1:
        progress = 0.0
    else:
        progress = frame / (gesture_frames - 1)

    # Get surrounding keyframes
    prev_kf, next_kf, interpolation_factor = find_surrounding_keyframes(
        gesture["keyframes"], progress
    )

    # Extract poses
    prev_pose = prev_kf["pose"]
    next_pose = next_kf["pose"]

    # Convert pose coordinates from lists to tuples
    prev_pose_tuples = {k: tuple(v) for k, v in prev_pose.items()}
    next_pose_tuples = {k: tuple(v) for k, v in next_pose.items()}

    # Interpolate
    result_pose = interpolate_pose(prev_pose_tuples, next_pose_tuples, interpolation_factor)

    # Fill in missing joints from default pose
    for joint in default_pose.keys():
        if joint not in result_pose:
            result_pose[joint] = default_pose[joint]

    return result_pose


def convert_pose_to_dict(pose: Dict[str, Tuple[float, float]]) -> Dict[str, List[float]]:
    """
    Convert pose from tuple format to list format for JSON serialization.

    Args:
        pose: Pose with tuple coordinates

    Returns:
        Pose with list coordinates
    """
    return {joint: list(coords) for joint, coords in pose.items()}


def convert_dict_to_pose(pose_dict: Dict[str, List[float]]) -> Dict[str, Tuple[float, float]]:
    """
    Convert pose from list format to tuple format for internal use.

    Args:
        pose_dict: Pose with list coordinates

    Returns:
        Pose with tuple coordinates
    """
    return {joint: tuple(coords) for joint, coords in pose_dict.items()}


# Exports
__all__ = [
    "linear_interpolate",
    "find_surrounding_keyframes",
    "interpolate_pose",
    "interpolate_gesture",
    "convert_pose_to_dict",
    "convert_dict_to_pose",
    "default_pose"
]
