# Stick Figure Avatar Engine - Flow Documentation

## Overview

The stick figure avatar engine converts sign language glosses into animated 2D stick figure visualizations using keyframe-based animation. This document explains the complete flow from input to rendered animation.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Stick Figure Avatar Engine                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │   Loader     │───▶│  Generator   │───▶│  Interpolator│    │
│  │              │    │              │    │              │    │
│  │ Loads JSON   │    │ Generates    │    │ Interpolates │    │
│  │ gestures     │    │ keypoint     │    │ between      │    │
│  │              │    │ sequences    │    │ keyframes    │    │
│  └──────────────┘    └──────────────┘    └──────────────┘    │
│         │                   │                      │          │
│         │                   │                      │          │
│         ▼                   ▼                      ▼          │
│  ┌──────────────────────────────────────────────────────┐    │
│  │         gestures/json/*.json (Gesture Files)          │    │
│  │         Renderer (Matplotlib/Streamlit)              │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Complete Flow

### Step 1: Initialization
```
User Input (Audio/Text) 
    ↓
Pipeline: process_audio_to_avatar(engine='stick')
    ↓
process_with_stick()
```

**What happens:**
- Audio is transcribed to text (if audio input)
- Text is converted to gloss sequence (e.g., ["HELLO", "I", "LOVE", "YOU"])
- Engine components are initialized:
  - `GestureLoader`: Loads all JSON gesture files (singleton pattern)
  - Gestures are cached in memory for fast access

### Step 2: Gesture Loading
```
Gloss Sequence: ["HELLO", "I", "LOVE", "YOU"]
    ↓
For each gloss:
    ↓
GestureLoader.gesture_exists(gloss)
    ↓
If exists: Load gesture JSON file
    ↓
Returns: Gesture definition with keyframes
```

**What happens:**
1. **GestureLoader** (singleton) loads all JSON files from `gestures/json/` on first access
2. Each JSON file is validated:
   - Must have `name`, `frames`, and `keyframes` fields
   - Keyframes must have `time` (0-1) and `pose` (joint coordinates)
   - Joints must be valid (LEFT/RIGHT_SHOULDER/ELBOW/WRIST)
3. Gestures are stored in memory dictionary keyed by name (uppercase)
4. `gesture_exists()` checks if gloss is available
5. `load_gesture()` retrieves the full gesture definition

**Example gesture structure:**
```json
{
  "name": "HELLO",
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
      "pose": { ... }
    }
  ]
}
```

### Step 3: Keypoint Generation
```
For each valid gloss:
    ↓
Generator.generate_keypoints(gloss, frames=30)
    ↓
For each frame (0 to frames-1):
    ↓
Interpolator.interpolate_gesture(gloss, frame, total_frames)
    ↓
Returns: Pose dictionary for that frame
```

**What happens:**
1. **Generator** calls `generate_keypoints(gloss, frames=30)`
2. For each frame (0 to 29):
   - Calculates progress: `progress = frame / (total_frames - 1)` (0.0 to 1.0)
   - Calls `interpolate_gesture()` to get pose for that progress
3. **Interpolator** finds surrounding keyframes:
   - Searches gesture's keyframes for prev/next keyframe
   - Calculates interpolation factor between them
4. **Interpolates** between keyframes:
   - Linear interpolation for each joint's x and y coordinates
   - Handles missing joints (uses default pose)
   - Returns complete pose dictionary
5. Returns list of 30 pose dictionaries (one per frame)

**Interpolation Example:**
```
Keyframe 1: time=0.0, RIGHT_WRIST=[0.5, 0.4]
Keyframe 2: time=1.0, RIGHT_WRIST=[0.6, 0.5]
Progress: 0.5 (middle frame)

Interpolated RIGHT_WRIST:
  x = 0.5 + (0.6 - 0.5) * 0.5 = 0.55
  y = 0.4 + (0.5 - 0.4) * 0.5 = 0.45
Result: [0.55, 0.45]
```

### Step 4: Frame Rendering
```
List of pose dictionaries (all_keypoints)
    ↓
For each pose:
    ↓
Renderer.render_avatar(pose, text=gloss)
    OR
Renderer.render_avatar_streamlit(placeholder, pose, text=gloss)
```

**What happens:**
1. **Renderer** draws stick figure using matplotlib:
   - **Head**: Circle at fixed position (0.5, 0.3)
   - **Body**: Line from (0.5, 0.35) to (0.5, 0.55)
   - **Arms**: Two segments per arm (shoulder→elbow, elbow→wrist)
   - **Hands**: Small circles at wrist positions
   - **Text**: Gesture label displayed above figure
2. For standard matplotlib: `render_avatar()` clears plot and redraws
3. For Streamlit: `render_avatar_streamlit()` renders to placeholder
4. Frame rate: ~30 FPS (0.03 second pause between frames)

**Coordinate System:**
- Normalized coordinates (0.0 to 1.0)
- (0.5, 0.5) is center
- Y-axis inverted (0.0 is top, 1.0 is bottom)
- X-axis: 0.0 is left, 1.0 is right

### Step 5: Display in Application
```
All keypoints generated
    ↓
Returned to Streamlit app
    ↓
Displayed in modal dialog
    ↓
Animated frame-by-frame
```

**What happens:**
1. All keypoints for all gestures are concatenated
2. Returned to Streamlit as `all_keypoints` list
3. Streamlit displays animation in modal dialog:
   - Creates empty placeholder
   - Loops through all keypoints
   - Renders each frame with `render_avatar_streamlit()`
   - Shows current gloss as text label
   - 0.03 second delay between frames

## Data Flow Diagram

```
┌─────────────┐
│ Audio Input │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ ASR (Whisper)   │ → Text: "Hello I love you"
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Text to Gloss   │ → ["HELLO", "I", "LOVE", "YOU"]
└──────┬──────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ GestureLoader                       │
│ - Check if "HELLO" exists           │
│ - Load gestures/json/hello.json     │
│ - Parse keyframes                   │
│ - Cache in memory                   │
│ - Repeat for each gloss             │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ Generator                           │
│ - For "HELLO": generate 30 frames  │
│ - For "I": generate 30 frames      │
│ - For "LOVE": generate 30 frames   │
│ - For "YOU": generate 30 frames    │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ Interpolator                        │
│ - For each frame:                   │
│   - Calculate progress (0-1)       │
│   - Find surrounding keyframes     │
│   - Interpolate joint positions     │
│   - Return pose dictionary          │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ Renderer                            │
│ - Draw head (circle)                │
│ - Draw body (line)                  │
│ - Draw arms (2 segments each)       │
│ - Draw hands (circles)              │
│ - Display text label                │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────┐
│ Animation   │
│ (120 frames)│
└─────────────┘
```

## Component Details

### GestureLoader (`loader.py`)
- **Purpose**: Loads and caches gesture definitions from JSON files
- **Pattern**: Singleton (one instance shared across application)
- **Key Methods**:
  - `gesture_exists(name)`: Check if gesture is available
  - `load_gesture(name)`: Get full gesture definition
  - `list_all_gestures()`: List all available gestures
- **Performance**: O(1) lookup using dictionary
- **Initialization**: Loads all JSON files on first access

### Generator (`generator.py`)
- **Purpose**: Generates keypoint sequences from gesture definitions
- **Key Methods**:
  - `generate_keypoints(gloss, frames=30)`: Generate frame sequence
  - `idle(frame, total)`: Default idle pose fallback
- **Behavior**:
  - Tries JSON gesture first
  - Falls back to IDLE pose if gesture not found
  - Returns list of pose dictionaries

### Interpolator (`interpolator.py`)
- **Purpose**: Interpolates between keyframes for smooth animation
- **Key Methods**:
  - `interpolate_gesture(name, frame, total_frames)`: Get pose for frame
  - `find_surrounding_keyframes(keyframes, progress)`: Find keyframes
  - `interpolate_pose(prev, next, factor)`: Linear interpolation
- **Algorithm**:
  - Linear interpolation: `value = start + (end - start) * t`
  - Handles edge cases (before first, after last keyframe)
  - Fills missing joints with default pose

### Renderer (`renderer.py`)
- **Purpose**: Visualizes stick figure using matplotlib
- **Two Modes**:
  1. **Standard**: `render_avatar(pose, text)` - For matplotlib plots
  2. **Streamlit**: `render_avatar_streamlit(placeholder, pose, text)` - For web
- **Drawing Elements**:
  - Head: Circle at (0.5, 0.3) with radius 0.05
  - Body: Line from (0.5, 0.35) to (0.5, 0.55)
  - Arms: Two segments per arm (shoulder→elbow, elbow→wrist)
  - Hands: Circles at wrist positions
  - Text: Label above figure (optional)

## Joint System

The stick figure uses 6 joints:

- **LEFT_SHOULDER**: Left shoulder position
- **LEFT_ELBOW**: Left elbow position
- **LEFT_WRIST**: Left wrist/hand position
- **RIGHT_SHOULDER**: Right shoulder position
- **RIGHT_ELBOW**: Right elbow position
- **RIGHT_WRIST**: Right wrist/hand position

**Default Pose** (used when joint missing):
```python
{
    "LEFT_SHOULDER": (0.45, 0.5),
    "LEFT_ELBOW": (0.45, 0.45),
    "LEFT_WRIST": (0.45, 0.4),
    "RIGHT_SHOULDER": (0.55, 0.5),
    "RIGHT_ELBOW": (0.55, 0.45),
    "RIGHT_WRIST": (0.55, 0.4)
}
```

## Error Handling & Fallbacks

1. **Missing Gesture**:
   - Gesture not found → Uses IDLE pose (default pose)
   - Warning logged, animation continues

2. **Invalid JSON**:
   - Malformed JSON → Error logged, gesture skipped
   - Missing required fields → Validation error, gesture skipped

3. **Missing Joints**:
   - Joint not in keyframe → Uses default pose value
   - Invalid joint name → Warning logged, joint ignored

4. **Invalid Coordinates**:
   - Out of bounds (0-1) → Warning logged, coordinates clamped

## Performance Characteristics

- **Gesture loading**: <0.1 seconds (one-time, cached)
- **Keypoint generation**: <0.01 seconds per gesture
- **Frame interpolation**: <0.001 seconds per frame
- **Frame rendering**: ~0.03 seconds per frame (30 FPS)
- **Total for 4 gestures**: ~0.1 seconds generation + 4 seconds rendering

## Integration Points

### With Pipeline (`pipeline/process_audio.py`)
```python
def process_with_stick(transcription, gloss_sequence):
    # Step 1: Check gestures exist
    # Step 2: Generate keypoints for each gloss
    # Step 3: Concatenate all keypoints
    # Step 4: Return for rendering
```

### With Streamlit (`app.py`)
```python
# User selects "stick" engine
result = process_audio_to_avatar(audio_path, engine='stick')
transcription, gloss_sequence, all_keypoints, valid_glosses = result

# Display animation in modal
show_results_dialog(..., all_keypoints=all_keypoints)
```

## Example Execution

```python
# Input
glosses = ["HELLO", "WORLD"]

# Step 1: Check gestures
from avatar_engines.stick import gesture_exists
for gloss in glosses:
    if gesture_exists(gloss):
        print(f"{gloss} exists")

# Step 2: Generate keypoints
from avatar_engines.stick import generate_keypoints
all_keypoints = []
for gloss in glosses:
    keypoints = generate_keypoints(gloss, frames=30)
    all_keypoints.extend(keypoints)
# Returns: List of 60 pose dictionaries

# Step 3: Render
from avatar_engines.stick import render_avatar
for i, pose in enumerate(all_keypoints):
    gloss_idx = i // 30
    render_avatar(pose, text=glosses[gloss_idx])
```

## Gesture File Structure

Each gesture is defined in a JSON file:

```json
{
  "name": "GESTURE_NAME",
  "description": "Optional description",
  "category": "Optional category",
  "frames": 30,
  "keyframes": [
    {
      "time": 0.0,
      "pose": {
        "LEFT_SHOULDER": [x, y],
        "LEFT_ELBOW": [x, y],
        "LEFT_WRIST": [x, y],
        "RIGHT_SHOULDER": [x, y],
        "RIGHT_ELBOW": [x, y],
        "RIGHT_WRIST": [x, y]
      }
    },
    {
      "time": 0.5,
      "pose": { ... }
    },
    {
      "time": 1.0,
      "pose": { ... }
    }
  ]
}
```

**Keyframe Rules:**
- `time` must be between 0.0 and 1.0
- First keyframe should have `time: 0.0`
- Last keyframe should have `time: 1.0`
- Keyframes are automatically sorted by time
- Coordinates are normalized (0.0 to 1.0)

## Summary

The stick figure avatar engine provides a complete pipeline from gloss sequences to animated visualizations:

1. **GestureLoader** → Loads gesture definitions from JSON
2. **Generator** → Generates keypoint sequences
3. **Interpolator** → Creates smooth animations between keyframes
4. **Renderer** → Draws stick figure visualization

All components work together seamlessly with automatic fallbacks, validation, and error handling to provide a robust sign language animation system.

