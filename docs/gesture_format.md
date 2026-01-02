# ASL JSON Gesture Format Documentation

## Overview

The ASL gesture system uses JSON files to define sign language gestures as keyframe animations. This document explains the format, structure, and best practices for creating and editing gesture definitions.

## Benefits of JSON Format

- **Human-readable**: Easy to understand and edit with any text editor
- **Version control**: Git-friendly format with clear diff visibility
- **Validation**: JSON schema ensures correctness
- **Portable**: Can be shared, imported, and exported
- **Tool-friendly**: Can be edited by GUI tools or programmatically

## File Structure

```
signs/gestures_json/
├── hello.json          # One gesture per file
├── mother.json
├── thank_you.json
└── ...
```

## JSON Schema

Each gesture file follows this structure:

```json
{
  "name": "GESTURE_NAME",
  "description": "Human-readable description",
  "category": "category_name",
  "tags": ["tag1", "tag2"],
  "frames": 30,
  "keyframes": [
    {
      "time": 0.0,
      "pose": {
        "JOINT_NAME": [x, y]
      }
    }
  ]
}
```

### Field Descriptions

#### `name` (required)
- Type: string
- The gesture name (e.g., "HELLO", "MOTHER")
- Should match the filename (lowercase with underscores)
- Must be unique across all gestures

#### `description` (optional)
- Type: string
- Human-readable description of the gesture
- Example: "Waving gesture for greeting"

#### `category` (optional)
- Type: string
- Used for organizing gestures
- Common categories: greetings, pronouns, verbs, objects, family, manners

#### `tags` (optional)
- Type: array of strings
- Additional classification tags
- Examples: ["common", "one-handed", "essential"]

#### `frames` (required)
- Type: integer
- Number of animation frames (typically 30)

#### `keyframes` (required)
- Type: array of keyframe objects
- Must have at least 1 keyframe
- Time values must be between 0.0 and 1.0
- Must be sorted by time value

### Keyframe Structure

```json
{
  "time": 0.5,
  "pose": {
    "RIGHT_WRIST": [0.6, 0.4],
    "LEFT_ELBOW": [0.45, 0.45]
  }
}
```

#### `time` (required)
- Type: number (0.0 to 1.0)
- Normalized time position
- 0.0 = beginning, 1.0 = end
- Intermediate values define motion timing

#### `pose` (required)
- Type: object mapping joints to coordinates
- Each joint maps to [x, y] coordinates
- Coordinates are normalized (0.0 to 1.0)

### Valid Joints

Only these joints can be defined:
- `LEFT_SHOULDER`
- `LEFT_ELBOW`
- `LEFT_WRIST`
- `RIGHT_SHOULDER`
- `RIGHT_ELBOW`
- `RIGHT_WRIST`

Any undefined joints will use default positions.

## Coordinate System

The avatar uses a normalized coordinate system:

- **Origin**: Top-left corner (0, 0)
- **X-axis**: 0.0 (left) to 1.0 (right)
- **Y-axis**: 0.0 (top) to 1.0 (bottom)
- **Avatar center**: (0.5, 0.5)

Default joint positions:
```
LEFT_SHOULDER:  (0.45, 0.5)
LEFT_ELBOW:     (0.45, 0.45)
LEFT_WRIST:     (0.45, 0.4)
RIGHT_SHOULDER: (0.55, 0.5)
RIGHT_ELBOW:    (0.55, 0.45)
RIGHT_WRIST:    (0.55, 0.4)
```

## Gesture Types

### 1. Static Gestures
Single keyframe representing a static hand position.

Example: MOTHER (touching chin)
```json
{
  "name": "MOTHER",
  "description": "Touch chin with fingertips",
  "category": "family",
  "frames": 30,
  "keyframes": [
    {
      "time": 0.0,
      "pose": {
        "RIGHT_WRIST": [0.52, 0.36]
      }
    }
  ]
}
```

### 2. Linear Motion
Two keyframes defining start and end positions.

Example: THANK-YOU (moving hand down)
```json
{
  "keyframes": [
    {
      "time": 0.0,
      "pose": {"RIGHT_WRIST": [0.55, 0.45]}
    },
    {
      "time": 1.0,
      "pose": {"RIGHT_WRIST": [0.55, 0.55]}
    }
  ]
}
```

### 3. Oscillating Gestures
Multiple keyframes creating back-and-forth motion.

Example: HELLO (waving hand side to side)
```json
{
  "keyframes": [
    {"time": 0.0, "pose": {"RIGHT_WRIST": [0.55, 0.4]}},
    {"time": 0.25, "pose": {"RIGHT_WRIST": [0.65, 0.4]}},
    {"time": 0.5, "pose": {"RIGHT_WRIST": [0.55, 0.4]}},
    {"time": 0.75, "pose": {"RIGHT_WRIST": [0.65, 0.4]}},
    {"time": 1.0, "pose": {"RIGHT_WRIST": [0.55, 0.4]}}
  ]
}
```

### 4. Circular Motion
Multiple keyframes creating circular path.

Example: PLEASE (circular motion on chest)
```json
{
  "keyframes": [
    {"time": 0.0, "pose": {"RIGHT_WRIST": [0.55, 0.45]}},
    {"time": 0.25, "pose": {"RIGHT_WRIST": [0.58, 0.48]}},
    {"time": 0.5, "pose": {"RIGHT_WRIST": [0.61, 0.45]}},
    {"time": 0.75, "pose": {"RIGHT_WRIST": [0.58, 0.42]}},
    {"time": 1.0, "pose": {"RIGHT_WRIST": [0.55, 0.45]}}
  ]
}
```

### 5. Two-Hand Gestures
Both hands moving simultaneously.

Example: BOOK (opening motion)
```json
{
  "keyframes": [
    {
      "time": 0.0,
      "pose": {
        "LEFT_WRIST": [0.47, 0.45],
        "RIGHT_WRIST": [0.53, 0.45]
      }
    },
    {
      "time": 1.0,
      "pose": {
        "LEFT_WRIST": [0.40, 0.45],
        "RIGHT_WRIST": [0.60, 0.45]
      }
    }
  ]
}
```

## Creating New Gestures

### Method 1: Manual JSON Creation

1. Choose a gesture name (e.g., "PLAY")
2. Determine if static, linear, or complex motion
3. Define keyframes with joint positions
4. Save as `play.json`

Example workflow:
```bash
cd signs/gestures_json/
cp hello.json play.json
# Edit play.json with your definitions
```

### Method 2: Using Migration Script

For converting Python gesture functions:

```bash
python scripts/migrate_gestures.py
```

This will automatically sample and convert all Python gestures to JSON.

### Method 3: Programmatic Generation

Use Python to generate keyframes:

```python
import json
import math

# Generate circular keyframes
def generate_circle(center_x, center_y, radius, num_points=8):
    keyframes = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        time = i / (num_points - 1)

        keyframes.append({
            "time": time,
            "pose": {"RIGHT_WRIST": [x, y]}
        })
    return keyframes

gesture = {
    "name": "CIRCLE",
    "description": "Circle motion",
    "category": "test",
    "frames": 30,
    "keyframes": generate_circle(0.5, 0.5, 0.1)
}

with open("circle.json", "w") as f:
    json.dump(gesture, f, indent=2)
```

## Best Practices

### 1. Keep it Simple
- Start with 1-3 keyframes for simple gestures
- Add more keyframes only for complex motions
- Avoid unnecessary joint definitions (use defaults)

### 2. Consistent Timing
- Use regular intervals for smooth animations
- Example: 0.0, 0.25, 0.5, 0.75, 1.0

### 3. Readable Format
- Include description and category
- Use meaningful gesture names
- Add helpful tags

### 4. Testing
- Test gestures individually before using in sentences
- Check for smooth motion (no jerky movements)
- Verify joints reach intended positions

### 5. Organization
- Group related gestures in categories
- Use consistent naming conventions
- Document complex gestures with comments (in separate doc)

## Validation

The system validates gestures on load:
- Required fields present
- Time values between 0.0-1.0
- Valid joint names
- Coordinate values between 0.0-1.0
- Keyframes sorted by time

Invalid gestures will log warnings but won't crash the system.

## Troubleshooting

### Gesture not loading
- Check JSON syntax (use a validator)
- Verify `name` field matches expectations
- Check console for validation errors

### Animation looks wrong
- Verify time values are sorted
- Check coordinate ranges
- Ensure sufficient keyframes for motion

### Motion too fast/slow
- Adjust `frames` value (higher = slower)
- Verify proportions in keyframe timing

## Migration from Python

The migration script converts Python functions:

```bash
python scripts/migrate_gestures.py
```

This:
1. Samples each Python gesture function
2. Detects static vs animated motion
3. Creates appropriate keyframes
4. Saves as JSON files
5. Preserves backward compatibility

You can still use Python gestures - the system falls back to them if JSON is missing.

## Example Files

See `signs/gestures_json/` for complete examples covering:
- 51 migrated gestures from Python
- Various motion types
- Different categories

Key examples to study:
- `hello.json` - oscillating motion
- `book.json` - two-handed gesture
- `mother.json` - static gesture
- `please.json` - circular motion
