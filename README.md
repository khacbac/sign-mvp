# Sign Language MVP

An automated sign language translation system that converts spoken audio into animated sign language gestures using an avatar renderer.

## Overview

This project provides an end-to-end pipeline for translating audio speech into American Sign Language (ASL) gestures:

1. **Speech Recognition (ASR)**: Transcribes audio files using OpenAI's Whisper model
2. **Natural Language Processing**: Converts English text to ASL gloss notation
3. **Gesture Generation**: Generates skeletal keypoint sequences for sign language gestures
4. **Avatar Rendering**: Visualizes signs using a 2D stick figure avatar with text labels

## Project Structure

```
sign_mvp/
├── asr/
│   └── transcribe.py          # Whisper-based audio transcription
├── nlp/
│   └── text_to_gloss.py       # Text-to-gloss conversion with ASL grammar rules
├── signs/
│   ├── gestures.py            # 50+ sign gesture definitions
│   ├── generator.py           # Keypoint sequence generator
│   └── avatar_renderer.py     # Matplotlib-based avatar visualization
├── input/                     # Sample audio files
│   ├── audio.wav
│   └── i_love_you.mp3
├── main.py                    # Full pipeline (audio → avatar)
├── demo_with_text.py          # Demo script with predefined glosses
└── environment.yml            # Conda environment specification
```

## Features

- 50+ ASL gesture vocabulary including:
  - Pronouns: ME, YOU, HE, SHE, WE, THEY
  - Questions: WHAT, WHERE, WHEN, WHY, WHO
  - Common verbs: LOVE, HELP, KNOW, SEE, GIVE, TAKE
  - Time expressions: NOW, TOMORROW, YESTERDAY, DAY
  - Greetings: HELLO, THANK-YOU, PLEASE, SORRY
  - Daily life: HOME, SCHOOL, WORK, FOOD, WATER

- ASL grammar conversion (removes English articles, auxiliary verbs, prepositions)
- Real-time avatar animation with gesture labels
- Modular pipeline design for easy extension

## Setup

### Prerequisites

- Python 3.10
- conda (Anaconda or Miniconda)
- ffmpeg (required by Whisper)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sign_mvp
```

2. Create and activate the conda environment:
```bash
conda env create -f environment.yml
conda activate sign_mvp
```

The environment includes:
- Python 3.10
- ffmpeg
- openai-whisper (20250625)
- matplotlib

## Usage

### Full Pipeline (Audio to Sign Language)

Run the complete pipeline from audio input:

```bash
python main.py input/audio.wav
```

This will:
1. Transcribe the audio file
2. Convert text to ASL gloss
3. Animate the avatar performing the signs

### Demo Mode (Predefined Sequence)

Run the demo with a hardcoded sign sequence:

```bash
python demo_with_text.py
```

This demonstrates the phrase "HELLO ME LOVE YOU" with animated gestures.

### Individual Modules

#### Transcribe Audio Only
```bash
python asr/transcribe.py input/audio.wav
```

#### Test Text-to-Gloss Conversion
```bash
python nlp/text_to_gloss.py
```

Example conversion:
- Input: "I want to drink water"
- Output: ['WANT', 'WATER']

## How It Works

### 1. Audio Transcription (asr/transcribe.py)

Uses OpenAI's Whisper model to convert speech to text:
- Default model: `base` (faster, reasonable accuracy)
- Other options: `tiny`, `small`, `medium`, `large` (slower, more accurate)

### 2. Text-to-Gloss Conversion (nlp/text_to_gloss.py)

Applies ASL grammar rules:
- Removes stopwords (articles, auxiliaries, prepositions)
- Uppercases words to gloss format
- Maps synonyms (e.g., "I" → "ME", "HI" → "HELLO")

Example transformations:
```
"I am drinking water" → ['WATER']
"Thank you for the help" → ['THANK-YOU', 'HELP']
"I love you" → ['ME', 'LOVE', 'YOU']
```

### 3. Gesture Generation (signs/generator.py)

Generates 30-frame keypoint sequences for each gloss using predefined gesture functions.

### 4. Avatar Rendering (signs/avatar_renderer.py)

Renders a stick figure avatar with:
- Head (circle)
- Body (vertical line)
- Arms (shoulder-elbow-wrist chain)
- Animated hand positions
- Text label showing current gesture

## Customization

### Adding New Gestures

1. Define the gesture function in `signs/gestures.py`:
```python
def new_gesture(frame, total):
    t = frame / total
    pose = base_pose()
    pose["RIGHT_WRIST"] = (x_position, y_position)
    return pose
```

2. Add to `GESTURE_MAP`:
```python
GESTURE_MAP = {
    ...
    "NEW-GESTURE": new_gesture,
}
```

### Adjusting Animation Speed

In `signs/generator.py`, modify the `frames` parameter:
```python
def generate_keypoints(gloss, frames=30):  # Increase for slower animation
```

### Changing Whisper Model Size

In `asr/transcribe.py` or when calling the function:
```python
text = transcribe_audio("input/audio.wav", model_size="medium")
```

## Limitations

- 2D stick figure visualization (not 3D realistic avatar)
- Limited gesture vocabulary (~50 signs)
- Simplified ASL grammar rules
- No facial expressions or non-manual markers
- Single-hand dominant gestures (limited two-hand coordination)
- No finger spelling support

## Future Enhancements

- Expand gesture vocabulary
- Add 3D avatar rendering
- Implement facial expressions
- Support for classifier constructions
- Real-time microphone input
- Video output export
- Web interface

## Dependencies

- `openai-whisper`: Speech recognition
- `matplotlib`: Avatar visualization
- `ffmpeg`: Audio processing backend

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]

## Acknowledgments

- OpenAI Whisper for speech recognition
- ASL linguistic resources for grammar rules
