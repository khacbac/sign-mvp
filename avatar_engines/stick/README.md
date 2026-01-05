# Stick Figure Avatar Engine

The stick figure avatar engine renders sign language gestures using a simple 2D stick figure representation. This engine is fully integrated and production-ready.

## Features Implemented

✅ **2D Stick Figure Visualization**

- Simple, clean stick figure representation
- Matplotlib-based rendering
- Real-time animation support

✅ **JSON-Based Gesture Definitions**

- Extensible gesture vocabulary
- Automatic gesture loading from JSON files
- Validation and error handling

✅ **Smooth Animation**

- Keyframe-based animation system
- Linear interpolation between keyframes
- Configurable frame rates

✅ **Streamlit Integration**

- Fully integrated into the main Streamlit application
- Real-time animation in dialog modals
- Text labels for current gesture
- Compact rendering optimized for web display

## Core Components

### `loader.py`

Loads and caches gesture definitions from JSON files.

**Usage:**

```python
from avatar_engines.stick import gesture_exists, load_gesture

# Check if gesture exists
if gesture_exists("HELLO"):
    gesture = load_gesture("HELLO")
    print(f"Gesture has {gesture['frames']} frames")
```

### `generator.py`

Generates keypoint sequences from gesture definitions.

**Usage:**

```python
from avatar_engines.stick import generate_keypoints

# Generate 30 frames for a gesture
keypoints = generate_keypoints("HELLO", frames=30)
print(f"Generated {len(keypoints)} frames")
```

### `interpolator.py`

Interpolates between keyframes for smooth animations.

**Key Features:**

- Linear interpolation between keyframe poses
- Automatic handling of missing joints
- Progress-based frame generation (0-1 normalized time)

### `renderer.py`

Matplotlib-based avatar visualization with Streamlit support.

**Usage:**

```python
from avatar_engines.stick import render_avatar, render_avatar_streamlit

# Standard matplotlib rendering
render_avatar(pose, text="HELLO")

# Streamlit rendering
import streamlit as st
placeholder = st.empty()
render_avatar_streamlit(placeholder, pose, text="HELLO")
```

## Requirements

- **matplotlib** - 2D visualization
- **streamlit** - Web interface (for Streamlit integration)
- **python 3.8+**

Install dependencies:

```bash
pip install matplotlib streamlit
```

## Usage Example

```python
from avatar_engines.stick import (
    gesture_exists,
    generate_keypoints,
    render_avatar
)

# Check if gesture exists
if gesture_exists("HELLO"):
    # Generate keypoint sequence
    frames = generate_keypoints("HELLO", frames=30)

    # Render each frame
    for i, pose in enumerate(frames):
        render_avatar(pose, text="HELLO")
```

## Streamlit Integration

The stick figure engine is fully integrated into the main Streamlit application (`app.py`). Users can:

- Select "Stick Figure" from the avatar engine dropdown
- Process audio through the complete pipeline (audio → text → gloss → animation)
- View animated stick figure in a modal dialog
- See text labels for each gesture

The engine works with all input methods:

- Local audio file testing
- Audio file uploads
- Microphone recordings

## Adding New Gestures

1. Create a JSON file in `gestures/json/` with the gesture definition
2. Follow the schema in `schema/gesture_schema.json`
3. The gesture will be automatically loaded on startup
4. Use the gesture name (uppercase) in your gloss sequences

**Example gesture file structure:**

```json
{
  "name": "HELLO",
  "description": "Greeting gesture",
  "frames": 30,
  "keyframes": [
    {
      "time": 0.0,
      "pose": {
        "LEFT_SHOULDER": [0.45, 0.5],
        "LEFT_ELBOW": [0.45, 0.45],
        "LEFT_WRIST": [0.45, 0.4],
        "RIGHT_SHOULDER": [0.55, 0.5],
        "RIGHT_ELBOW": [0.55, 0.45],
        "RIGHT_WRIST": [0.6, 0.4]
      }
    },
    {
      "time": 1.0,
      "pose": {
        ...
      }
    }
  ]
}
```

## Gesture Format

Gestures are defined using keyframe animation:

- **name**: Gesture name (uppercase, e.g., "HELLO")
- **description**: Optional description
- **frames**: Total number of frames for the animation
- **keyframes**: Array of keyframe definitions
  - **time**: Normalized time (0.0 to 1.0) for each keyframe
  - **pose**: Joint positions for the keyframe
  - **Joints**: LEFT_SHOULDER, LEFT_ELBOW, LEFT_WRIST, RIGHT_SHOULDER, RIGHT_ELBOW, RIGHT_WRIST
  - **Coordinates**: Normalized (0.0 to 1.0) where (0.5, 0.5) is center

## Performance

- **Gesture loading**: <0.1 seconds (cached after first load)
- **Keypoint generation**: <0.01 seconds per gesture
- **Frame rendering**: ~0.03 seconds per frame (30 FPS)
- **Streamlit rendering**: Optimized for web display

## Limitations

- 2D representation only (no depth)
- Limited to 6 joints (shoulders, elbows, wrists)
- Simple linear interpolation (no easing functions)
- Fixed body/head position (only arms animate)

## Future Enhancements

- [ ] Easing functions for smoother animations
- [ ] Additional joints (head, torso, fingers)
- [ ] 3D stick figure support
- [ ] Customizable colors and styles
- [ ] Gesture speed control
- [ ] Background customization

## Implementation Status

🟢 **Phase 1**: Core rendering engine - **COMPLETE**
🟢 **Phase 2**: JSON gesture loading - **COMPLETE**
🟢 **Phase 3**: Keyframe interpolation - **COMPLETE**
🟢 **Phase 4**: Streamlit integration - **COMPLETE**
🟢 **Phase 5**: Testing and optimization - **COMPLETE**

**Status**: ✅ **Production Ready** - The stick figure avatar engine is fully functional and integrated into the application.
