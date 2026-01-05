"""
JSON Gesture Loader

Loads and caches gesture definitions from JSON files.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

# Joint names that can be defined in gestures
VALID_JOINTS = {
    "LEFT_SHOULDER", "LEFT_ELBOW", "LEFT_WRIST",
    "RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"
}


class GestureLoader:
    """Singleton class for loading and caching gesture definitions from JSON files"""

    _instance = None
    _gestures = None
    _gestures_dir = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._gestures is None:
            self._gestures = {}
            self._load_all_gestures()

    def _load_all_gestures(self):
        """Load all gesture JSON files from the gestures directory"""
        # Get the gestures directory relative to this file
        current_dir = Path(__file__).parent
        self._gestures_dir = current_dir / "gestures" / "json"

        if not self._gestures_dir.exists():
            logger.warning(f"Gestures directory not found: {self._gestures_dir}")
            return

        # Load all JSON files
        json_files = list(self._gestures_dir.glob("*.json"))
        logger.info(f"Found {len(json_files)} gesture files in {self._gestures_dir}")

        for json_file in json_files:
            try:
                gesture = self._load_gesture_file(json_file)
                if gesture:
                    self._gestures[gesture["name"]] = gesture
                    logger.debug(f"Loaded gesture: {gesture['name']}")
            except Exception as e:
                logger.error(f"Error loading {json_file}: {e}")

        logger.info(f"Successfully loaded {len(self._gestures)} gestures")

    def _load_gesture_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """Load a single gesture from a JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                gesture = json.load(f)

            # Basic validation
            if "name" not in gesture:
                raise ValueError("Missing required field: name")

            if "frames" not in gesture:
                raise ValueError("Missing required field: frames")

            if "keyframes" not in gesture:
                raise ValueError("Missing required field: keyframes")

            if not isinstance(gesture["keyframes"], list) or len(gesture["keyframes"]) == 0:
                raise ValueError("Keyframes must be a non-empty list")

            # Validate keyframe structure
            for i, keyframe in enumerate(gesture["keyframes"]):
                if "time" not in keyframe:
                    raise ValueError(f"Keyframe {i}: missing required field: time")

                if "pose" not in keyframe:
                    raise ValueError(f"Keyframe {i}: missing required field: pose")

                # Validate time is between 0 and 1
                time = keyframe["time"]
                if not (0 <= time <= 1):
                    raise ValueError(f"Keyframe {i}: time must be between 0 and 1, got {time}")

                # Validate pose joints
                for joint, coords in keyframe["pose"].items():
                    if joint not in VALID_JOINTS:
                        logger.warning(f"Unknown joint '{joint}' in {gesture['name']}, keyframe {i}")

                    if not isinstance(coords, list) or len(coords) != 2:
                        raise ValueError(f"Keyframe {i}, joint {joint}: coordinates must be [x, y] list")

                    x, y = coords
                    if not (0 <= x <= 1 and 0 <= y <= 1):
                        logger.warning(f"Joint {joint} coordinates out of bounds [0,1]: [{x}, {y}]")

            # Sort keyframes by time
            gesture["keyframes"].sort(key=lambda k: k["time"])

            return gesture

        except Exception as e:
            logger.error(f"Failed to load gesture from {file_path}: {e}")
            return None

    def get_gesture(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a gesture by name"""
        return self._gestures.get(name.upper())

    def list_gestures(self) -> List[str]:
        """List all available gesture names"""
        return sorted(self._gestures.keys())

    def gesture_exists(self, name: str) -> bool:
        """Check if a gesture exists"""
        return name.upper() in self._gestures

    def reload_gestures(self):
        """Reload all gestures (useful for development)"""
        self._gestures = {}
        self._load_all_gestures()

    def get_gesture_count(self) -> int:
        """Get the number of loaded gestures"""
        return len(self._gestures)


# Global loader instance
_gesture_loader = GestureLoader()


def load_gesture(name: str) -> Optional[Dict[str, Any]]:
    """Convenience function to load a single gesture"""
    return _gesture_loader.get_gesture(name)


def list_all_gestures() -> List[str]:
    """Convenience function to list all gesture names"""
    return _gesture_loader.list_gestures()


def gesture_exists(name: str) -> bool:
    """Convenience function to check if a gesture exists"""
    return _gesture_loader.gesture_exists(name)


def get_available_gestures_count() -> int:
    """Get the total number of available gestures"""
    return _gesture_loader.get_gesture_count()


# Exports
__all__ = [
    "GestureLoader",
    "load_gesture",
    "list_all_gestures",
    "gesture_exists",
    "get_available_gestures_count",
    "VALID_JOINTS"
]
