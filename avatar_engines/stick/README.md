# Stick Figure Avatar Engine

The stick figure avatar engine renders sign language gestures using a simple 2D stick figure representation.

## Features

- 2D stick figure visualization
- JSON-based gesture definitions
- Smooth interpolation between keyframes
- Text labels for current gesture
- Extensible gesture vocabulary

## Components

- `renderer.py` - Matplotlib-based avatar visualization
- `generator.py` - Generates keypoint sequences from gesture definitions
- `interpolator.py` - Interpolates between keyframes for smooth animations
- `loader.py` - Loads and caches gesture definitions from JSON files
- `gestures/json/` - JSON gesture definition files

## Usage

```python
from avatar_engines.stick import generate_keypoints, render_avatar

# Generate keypoints for a gesture
frames = generate_keypoints("HELLO")

# Render a single frame
render_avatar(frames[0], text="HELLO")
```

## Adding New Gestures

1. Create a JSON file in `gestures/json/` with the gesture definition
2. Follow the schema in `schema/gesture_schema.json`
3. The gesture will be automatically loaded on startup

## Gesture Format

Gestures are defined using keyframe animation:
- `time`: Normalized time (0 to 1) for each keyframe
- `pose`: Joint positions for the keyframe
- Joints: LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST, RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST
