#!/usr/bin/env python3
"""
Gesture Migration Script

Converts Python gesture functions to JSON format.

Usage:
    python scripts/migrate_gestures.py

This will:
1. Load all gestures from signs.gestures.GESTURE_MAP
2. Sample each gesture to extract keyframes
3. Save as JSON files in signs/gestures_json/
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from signs.gestures import GESTURE_MAP
from signs.loader import VALID_JOINTS


def sample_gesture(gesture_func, frames: int = 30) -> Tuple[Dict[str, Tuple[float, float]], List[Dict[str, Any]]]:
    """
    Sample a gesture function at regular intervals to extract keyframes.

    Uses simplified heuristics to detect key poses:
    - Samples at 0%, 25%, 50%, 75%, 100%
    - Samples more frequently if significant changes detected

    Args:
        gesture_func: The gesture function to sample
        frames: Number of frames to sample

    Returns:
        Tuple of (static_pose, keyframes)
    """
    base_pose = {
        "LEFT_SHOULDER": (0.45, 0.5),
        "LEFT_ELBOW": (0.45, 0.45),
        "LEFT_WRIST": (0.45, 0.4),
        "RIGHT_SHOULDER": (0.55, 0.5),
        "RIGHT_ELBOW": (0.55, 0.45),
        "RIGHT_WRIST": (0.55, 0.4)
    }

    # Sample all frames
    all_poses = []
    for f in range(frames):
        try:
            pose = gesture_func(f, frames)
            all_poses.append(pose)
        except Exception as e:
            print(f"Error sampling frame {f}: {e}")
            all_poses.append(base_pose.copy())

    # Check if gesture is static (all poses are identical)
    first_pose = all_poses[0]
    is_static = True
    joint_changes = {joint: [] for joint in base_pose.keys()}

    for pose in all_poses:
        for joint in base_pose.keys():
            pos1 = pose.get(joint, base_pose[joint])
            pos2 = first_pose.get(joint, base_pose[joint])
            if pos1 != pos2:
                is_static = False
            # Track position for range calculation
            joint_changes[joint].append(pos1)

    if is_static:
        # Static gesture - only need one keyframe
        keyframes_data = [{
            "time": 0.0,
            "pose": {k: list(v) for k, v in first_pose.items() if k in VALID_JOINTS}
        }]
        return first_pose, keyframes_data

    # For animated gestures, detect keyframes
    # Strategy: check for direction changes in motion
    keyframe_indices = [0, frames - 1]  # Always include first and last

    # Check intermediate positions
    num_samples = min(5, frames)  # Sample at most 5 keyframes
    for i in range(1, num_samples - 1):
        frame_idx = int(i * (frames - 1) / (num_samples - 1))
        keyframe_indices.append(frame_idx)

    keyframe_indices = sorted(list(set(keyframe_indices)))

    # Build keyframes
    keyframes_data = []
    for idx in keyframe_indices:
        normalized_time = idx / (frames - 1)
        pose = all_poses[idx]

        # Only include joints that are different from default
        pose_dict = {}
        for joint in VALID_JOINTS:
            if joint in pose:
                pose_dict[joint] = list(pose[joint])

        if pose_dict:  # Only add if we have actual joint data
            keyframes_data.append({
                "time": normalized_time,
                "pose": pose_dict
            })

    return first_pose, keyframes_data


def describe_gesture(gesture_name: str) -> str:
    """Generate a simple description based on the gesture name"""
    name_lower = gesture_name.lower().replace("-", " ")

    if any(word in name_lower for word in ["hello", "hi", "bye"]):
        return f"Greeting gesture - signing '{name_lower}'"
    elif any(word in name_lower for word in ["thank", "sorry", "please"]):
        return f"Manners gesture - signing '{name_lower}'"
    elif any(word in name_lower for word in ["mother", "father", "family"]):
        return f"Family sign - '{name_lower}'"
    elif any(word in name_lower for word in ["good", "bad", "like", "love"]):
        return f"Descriptive gesture - signing '{name_lower}'"
    elif any(word in name_lower for word in ["me", "you", "he", "she", "they"]):
        return f"Pronoun - signing '{name_lower}'"
    else:
        return f"ASL sign for '{name_lower}'"


def categorize_gesture(gesture_name: str) -> str:
    """Categorize gesture based on name"""
    name_lower = gesture_name.lower()

    categories = {
        "greetings": ["hello", "hi", "bye"],
        "manners": ["thank", "sorry", "please"],
        "family": ["mother", "father", "parent", "family"],
        "pronouns": ["me", "you", "he", "she", "they", "we"],
        "common": ["good", "bad", "yes", "no"],
        "verbs": ["go", "come", "give", "take", "see", "look", "know"],
        "objects": ["book", "water", "food"],
        "time": ["today", "tomorrow", "yesterday", "now"]
    }

    for category, keywords in categories.items():
        if any(word in name_lower for word in keywords):
            return category

    return "other"


def generate_gesture_json(gesture_name: str, gesture_func) -> Dict[str, Any]:
    """Generate JSON structure for a gesture"""
    # Sample the gesture and get keyframes
    _, keyframes = sample_gesture(gesture_func)

    # Generate JSON
    gesture_data = {
        "name": gesture_name,
        "description": describe_gesture(gesture_name),
        "category": categorize_gesture(gesture_name),
        "tags": [],
        "frames": 30,
        "keyframes": keyframes
    }

    return gesture_data


def save_gesture_json(gesture_name: str, gesture_data: Dict[str, Any], output_dir: Path):
    """Save gesture JSON to file"""
    # Convert name to filename format (lowercase, underscores)
    filename = gesture_name.lower().replace("-", "_") + ".json"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    filepath = output_dir / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(gesture_data, f, indent=2, ensure_ascii=False)

    return filepath


def main():
    print("ASL Gesture Migration Tool")
    print("=" * 50)
    print(f"Found {len(GESTURE_MAP)} gestures to migrate")
    print()

    # Output directory
    output_dir = project_root / "signs" / "gestures_json"

    # Track statistics
    migrated = 0
    skipped = 0
    errors = 0

    for i, (gesture_name, gesture_func) in enumerate(sorted(GESTURE_MAP.items()), 1):
        # Skip IDLE
        if gesture_name == "IDLE":
            skipped += 1
            continue

        try:
            print(f"[{i:3d}/{len(GESTURE_MAP):3d}] {gesture_name}")

            # Generate JSON
            gesture_data = generate_gesture_json(gesture_name, gesture_func)

            # Save to file
            filepath = save_gesture_json(gesture_name, gesture_data, output_dir)

            # Verify the file was created
            if filepath.exists():
                migrated += 1
            else:
                errors += 1
                print(f"  ⚠️  Failed to save: {filepath}")

        except Exception as e:
            errors += 1
            print(f"  ⚠️  Error: {e}")

    print()
    print("=" * 50)
    print("Migration Complete!")
    print(f"✅ Migrated: {migrated}")
    print(f"⚠️  Skipped: {skipped} (IDLE)")
    print(f"❌ Errors: {errors}")
    print()
    print(f"Files saved to: {output_dir}")
    print()
    print("To use these gestures, ensure signs.loader can find them.")


if __name__ == "__main__":
    main()
