# Sign Language Translation System

An end-to-end system that converts spoken audio into American Sign Language (ASL) gestures using multiple avatar rendering engines.

## Key Features

- **65+ ASL Gestures** with intelligent fallback system (FINGERSPELL, UNKNOWN placeholders)
- **3 Avatar Engines**: Stick figure (2D), Skeleton (3D poses), Human Video (WLASL dataset)
- **Multiple Interfaces**: Streamlit web app, CLI, Flask REST API, FastAPI service, React pose viewer
- **Complete Pipeline**: Audio → Whisper transcription → NLP gloss conversion → Avatar animation
- **Production-Ready**: Enhanced NLP with 136+ synonym mappings, text chunking, comprehensive error handling

---

## Quick Start

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

3. **(Optional)** Install additional dependencies for specific engines:

   ```bash
   # For Human Video engine
   pip install moviepy>=1.0.3 yt-dlp>=2024.12.13

   # For Streamlit web interface
   pip install streamlit>=1.29.0 streamlit-audiorecorder

   # For Flask API
   pip install flask
   ```

### Run Your First Translation

#### 1. Web Interface (Streamlit) - **RECOMMENDED**

```bash
streamlit run app.py
```

Then:

- Upload an audio file or record your voice
- Enter text directly
- Choose avatar engine (stick/skeleton/human_video)
- Watch the ASL animation!

#### 2. Command Line

```bash
# Using stick figure engine (default)
python main.py input/audio.wav

# Using human video engine
python pipeline/process_audio.py  # See usage in file
```

#### 3. API Usage

```python
from pipeline.process_audio import process_audio_to_avatar

transcription, gloss, result, valid = process_audio_to_avatar(
    "input/audio.wav",
    engine="stick"  # or "skeleton", "human_video"
)
```

---

## Project Architecture

### System Overview

```
Audio Input
    ↓
[ASR Module] → Whisper (medium model) → Transcribed Text
    ↓
[NLP Module] → Stopword removal, synonym mapping, ASL grammar → Gloss Sequence
    ↓
[Avatar Engine Selection]
    ├→ [Stick] → 2D matplotlib animation
    ├→ [Skeleton] → 3D pose files via FastAPI
    └→ [Human Video] → WLASL video composition
    ↓
Animated Avatar Output
```

### Component Breakdown

1. **Speech Recognition** (`asr/`)

   - `transcribe.py`: Whisper-based audio transcription (medium model)
   - Supports: tiny, base, small, medium, large models

2. **Natural Language Processing** (`nlp/`)

   - `text_to_gloss.py`: English → ASL gloss conversion
   - 40+ stopwords removed
   - 136+ synonym mappings
   - Text chunking (max 15 words per chunk)
   - Input validation (max 1000 characters)

3. **Avatar Engines** (`avatar_engines/`)

   - **Stick** (`stick/`): 2D matplotlib stick figure with JSON gesture definitions
   - **Skeleton** (`skeleton/`): 3D pose generation via FastAPI service
   - **Human Video** (`human_video/`): Real WLASL sign language videos

4. **Pipeline** (`pipeline/`)

   - `process_audio.py`: Orchestrates the complete workflow with multi-engine support

5. **Interfaces**
   - `app.py`: Streamlit web application
   - `main.py`: Command-line interface
   - `api.py`: Flask REST API
   - `text-to-skeleton/`: FastAPI service for 3D poses
   - `pose-viewer/`: React app for pose visualization

### Directory Structure

```
sign_mvp/
├── asr/                          # Speech recognition
│   └── transcribe.py
├── nlp/                          # NLP & gloss conversion
│   └── text_to_gloss.py
├── avatar_engines/               # Rendering engines
│   ├── stick/                    # 2D stick figure (MAIN)
│   │   ├── gestures/json/        # 65 gesture definitions
│   │   ├── schema/               # JSON schema validation
│   │   ├── renderer.py           # Matplotlib rendering
│   │   ├── generator.py          # Keypoint generation with fallbacks
│   │   ├── interpolator.py       # Smooth animation
│   │   └── loader.py             # Gesture loader (singleton)
│   ├── skeleton/                 # 3D skeleton via FastAPI
│   │   └── client.py             # HTTP client
│   └── human_video/              # WLASL video-based
│       ├── gloss_mapper.py       # Gloss → video mapping
│       ├── video_loader.py       # Downloads WLASL videos
│       └── video_compositor.py   # Video composition
├── pipeline/                     # Processing pipeline
│   └── process_audio.py          # Main pipeline with multi-engine support
├── text-to-skeleton/            # FastAPI 3D pose service
│   ├── main.py                   # FastAPI app
│   ├── generate_poses.py         # Pose generation
│   └── assets/                   # Lexicon data
├── pose-viewer/                 # React pose visualizer
│   ├── src/
│   └── public/
├── utils/                        # Utilities
│   └── logging_config.py         # Centralized logging
├── input/                        # Sample audio files
├── app.py                        # Streamlit web app
├── main.py                       # CLI entry point
├── api.py                        # Flask REST API
└── environment.yml              # Conda environment
```

---

## Avatar Engines Comparison

| Feature              | Stick                     | Skeleton         | Human Video             |
| -------------------- | ------------------------- | ---------------- | ----------------------- |
| **Realism**          | ⭐                        | ⭐⭐             | ⭐⭐⭐⭐⭐              |
| **Speed**            | ⭐⭐⭐⭐⭐                | ⭐⭐⭐           | ⭐⭐                    |
| **Setup Complexity** | Easy                      | Medium           | Easy                    |
| **Dependencies**     | matplotlib                | FastAPI service  | moviepy, yt-dlp         |
| **Output Format**    | Live animation            | .pose file       | MP4 video               |
| **Vocabulary**       | 65 gestures               | Lexicon-based    | 2000+ WLASL signs       |
| **Fallback Support** | ✅ (FINGERSPELL, UNKNOWN) | ✅               | ✅ (Alternative videos) |
| **Best For**         | Quick prototyping         | 3D visualization | Production/demos        |

---

## Usage Guides

### 1. Streamlit Web App

```bash
streamlit run app.py
```

**Features:**

- Upload audio files or record via microphone
- Enter text directly (skips ASR)
- Choose from 3 avatar engines
- Real-time animation display
- Downloadable video output (human_video engine)

**Avatar Engine Selection:**

- **Stick**: Instant 2D animation
- **Skeleton**: Generates `.pose` file in `text-to-skeleton/output/poses/`
- **Human Video**: Downloads and composites WLASL videos

### 2. Command Line Interface

```bash
# Process audio with default stick engine
python main.py input/audio.wav

# Using the pipeline module directly
python -c "from pipeline.process_audio import process_audio_to_avatar; \
process_audio_to_avatar('input/audio.wav', engine='stick')"
```

### 3. Flask API

Start the API server:

```bash
python api.py
```

**Endpoints:**

- `GET /api/health` - Health check
- `GET /api/pose/sample` - Get sample pose
- `GET /api/pose/list` - List available poses

**Example:**

```bash
curl http://localhost:5000/api/health
```

### 4. FastAPI Service (Skeleton Engine)

Start the skeleton service:

```bash
cd text-to-skeleton
uvicorn main:app --reload
```

**Endpoints:**

- `GET /text-to-gloss?text=...` - Convert text to gloss
- `GET /text-to-pose?text=...` - Generate pose file
- `GET /text-to-video?text=...` - Generate video

**Example:**

```bash
curl "http://localhost:8000/text-to-gloss?text=hello%20world"
```

Pose files are saved to: `text-to-skeleton/output/poses/{filename}.pose`

### 5. React Pose Viewer

```bash
cd pose-viewer
npm install
npm run dev
```

View `.pose` files generated by the skeleton engine. See [pose-viewer/README.md](pose-viewer/README.md) for details.

---

## Gesture System

### Available Gestures (65+)

Organized by category:

**Pronouns**: ME, YOU, HE, SHE, WE, THEY

**Questions**: WHAT, WHERE, WHEN, WHY, WHO, HOW

**Common Verbs**: LOVE, HELP, KNOW, SEE, GIVE, TAKE, WANT, EAT, DRINK, GO, COME, MAKE, WORK, PLAY, THINK, FEEL, NEED

**Time Expressions**: NOW, TOMORROW, YESTERDAY, DAY, WEEK, MONTH, YEAR, TODAY, TONIGHT, MORNING, AFTERNOON, EVENING

**Greetings & Courtesy**: HELLO, GOODBYE, THANK-YOU, PLEASE, SORRY, YES, NO, OK, WELCOME

**Daily Life**: HOME, SCHOOL, WORK, FOOD, WATER, BOOK, CAR, HOUSE, FAMILY, FRIEND, MOTHER, FATHER, CHILD

**Emotions**: HAPPY, SAD, ANGRY, LOVE, FEAR

**Fallback Gestures**:

- `FINGERSPELL`: For short words (≤3 characters)
- `UNKNOWN`: For longer unknown words
- `IDLE`: Default rest pose

### Fallback System

The system intelligently handles unknown words:

1. **Short words (≤3 chars)** → `FINGERSPELL` placeholder
2. **Longer unknown words** → `UNKNOWN` placeholder
3. **WLASL engine** → Searches alternatives and fallback videos
4. **Last resort** → `IDLE` pose

**Example:**

- Input: "I love NYC"
- Gloss: `['ME', 'LOVE', 'NYC*']` (`*` indicates FINGERSPELL fallback)

### Adding Custom Gestures

Create a JSON file in `avatar_engines/stick/gestures/json/`:

```json
{
  "name": "CUSTOM",
  "description": "My custom gesture",
  "category": "custom",
  "frames": 30,
  "keyframes": [
    {
      "time": 0.0,
      "pose": {
        "RIGHT_SHOULDER": [0.4, 0.3],
        "RIGHT_ELBOW": [0.35, 0.45],
        "RIGHT_WRIST": [0.3, 0.6],
        "LEFT_SHOULDER": [0.6, 0.3],
        "LEFT_ELBOW": [0.65, 0.45],
        "LEFT_WRIST": [0.7, 0.6]
      }
    }
  ]
}
```

See [docs/gesture_format.md](docs/gesture_format.md) for complete schema and examples.

---

## Configuration

### Environment Variables

No environment variables required for basic usage. Optional:

```bash
export WHISPER_MODEL_SIZE=medium  # tiny, base, small, medium, large
```

### Module Configuration

**NLP Settings** (`nlp/text_to_gloss.py`):

```python
DEFAULT_MAX_CHUNK_WORDS = 15  # Words per chunk
MAX_INPUT_LENGTH = 1000        # Max input characters
```

**Animation Settings** (`avatar_engines/stick/generator.py`):

```python
DEFAULT_ANIMATION_FRAMES = 30     # Frames per gesture
FINGERSPELL_MAX_LENGTH = 3        # Chars for fingerspell fallback
```

**Video Settings** (`avatar_engines/human_video/video_compositor.py`):

```python
MAX_GLOSSES_IN_FILENAME = 5       # Glosses in filename
MAX_FILENAME_LENGTH = 50          # Max filename length
```

---

## API Reference

### Python API

#### `process_audio_to_avatar(audio_path, engine='stick')`

Complete pipeline: Audio → Avatar

**Parameters:**

- `audio_path` (str): Path to audio file
- `engine` (str): 'stick', 'skeleton', or 'human_video'

**Returns:**

- `transcription` (str): Transcribed text
- `gloss_sequence` (list): ASL gloss sequence
- `result_data`: Engine-specific (keypoints, path, or None)
- `valid_glosses` (list): Glosses with gesture data

**Example:**

```python
from pipeline.process_audio import process_audio_to_avatar

text, gloss, keypoints, valid = process_audio_to_avatar(
    "input/audio.wav",
    engine="stick"
)
print(f"Transcription: {text}")
print(f"Gloss: {gloss}")
```

#### `process_text_to_avatar(text, engine='stick')`

Process text directly (skip ASR).

**Example:**

```python
from pipeline.process_audio import process_text_to_avatar

text, gloss, result, valid = process_text_to_avatar(
    "I love you",
    engine="stick"
)
```

### REST API (Flask)

**Base URL:** `http://localhost:5000`

| Endpoint           | Method | Description          |
| ------------------ | ------ | -------------------- |
| `/api/health`      | GET    | Health check         |
| `/api/pose/sample` | GET    | Get sample pose data |
| `/api/pose/list`   | GET    | List available poses |

### FastAPI Endpoints (Skeleton)

**Base URL:** `http://localhost:8000`

| Endpoint         | Method | Parameters   | Returns               |
| ---------------- | ------ | ------------ | --------------------- |
| `/text-to-gloss` | GET    | `text` (str) | Gloss sequence (JSON) |
| `/text-to-pose`  | GET    | `text` (str) | Pose file path        |
| `/text-to-video` | GET    | `text` (str) | Video file path       |

---

## Technical Details

### Pipeline Flow

```
1. Audio Input (WAV, MP3)
   ↓
2. Whisper Transcription
   - Model: medium (1.5GB download on first run)
   - Language: Auto-detect
   - Output: Raw English text
   ↓
3. Text-to-Gloss Conversion
   - Remove 40+ stopwords (articles, aux verbs, prepositions)
   - Apply 136+ synonym mappings (I→ME, DRINKING→WATER, etc.)
   - Chunk long text (max 15 words)
   - Validate input (max 1000 chars)
   ↓
4. Gesture Generation
   [Stick Engine]
   - Load JSON gestures from disk (singleton cache)
   - Interpolate keyframes → 30-frame sequences
   - Apply fallback for unknown words

   [Skeleton Engine]
   - Call FastAPI service with text
   - Service uses spaCy for lemmatization
   - Generates .pose file with 3D coordinates

   [Human Video Engine]
   - Map glosses to WLASL video IDs
   - Download videos via yt-dlp (cached)
   - Composite with moviepy
   ↓
5. Output
   - Stick: Live matplotlib animation
   - Skeleton: .pose file
   - Human Video: MP4 composite video
```

### Text-to-Gloss Conversion

**Stopword Removal:**

- Articles: the, a, an
- Auxiliaries: is, are, am, do, does, was, were
- Prepositions: in, on, at, to, from, with
- Conjunctions: and, but, or

**Synonym Mapping Examples:**

- Pronouns: I → ME, MY → ME, MINE → ME
- Tenses: DRINKING → WATER, EATING → EAT
- Phrases: DONT → NO, CANT → NO, WONT → NO

**ASL Grammar Rules:**

- Topic-comment structure (simplified)
- Subject-object-verb order (simplified)
- No verb conjugations
- Time expressions at beginning

### Keypoint Animation System

**Skeleton Structure:**

- 6 keypoints: LEFT/RIGHT_SHOULDER, ELBOW, WRIST
- Normalized coordinates: [0, 1] range
- Default pose: Arms at rest

**Interpolation:**

- Linear interpolation between keyframes
- Time-based blending: `pose = lerp(kf1, kf2, t)`
- Smooth transitions (30 FPS)

**Rendering:**

- Matplotlib backend (stick engine)
- Real-time frame updates
- Text overlay for current gesture

### Video Composition (Human Video Engine)

**WLASL Integration:**

- Dataset: 2000+ sign language videos
- Source: YouTube + supplementary videos
- Metadata: JSON with video IDs, glosses, start/end times

**Video Processing:**

- Download via yt-dlp (fallback to alternatives)
- Cache videos locally
- Concatenate with moviepy
- Resize and crop to standard dimensions

**Fallback Logic:**

1. Try primary video source
2. Try up to 3 alternative videos
3. Skip if all downloads fail
4. Continue with available videos

---

## Development

### Running Tests

```bash
python test_improvements.py
```

Tests cover:

- NLP gloss conversion
- Gesture loading and interpolation
- Fallback mechanisms
- Pipeline integration

### Project Structure Patterns

**Design Patterns:**

- **Singleton**: GestureLoader (caches 65 gestures)
- **Factory**: Avatar engine selection
- **Strategy**: Multiple rendering engines

**Code Organization:**

- Modular architecture (ASR, NLP, Avatar separate)
- Centralized logging (`utils/logging_config.py`)
- Configuration constants at module level
- Clear separation of concerns

### Contributing

1. Follow existing code style
2. Add logging for debugging
3. Use constants instead of magic numbers
4. Update tests for new features
5. Document new gestures in JSON format

---

## Troubleshooting

### Common Issues

**Whisper model download (first run):**

- Model downloads ~1GB on first use
- Check internet connection
- Model cached in `~/.cache/whisper/`

**Video download fails (human_video engine):**

- Install: `pip install yt-dlp moviepy`
- Check YouTube availability
- Videos cached in `avatar_engines/human_video/cache/`

**Skeleton service unavailable:**

- Start FastAPI: `cd text-to-skeleton && uvicorn main:app --reload`
- Service runs on `http://localhost:8000`
- Check dependencies: `pip install fastapi uvicorn spacy`

**Import errors:**

- Ensure conda environment is activated: `conda activate sign_mvp`
- Project root should be in PYTHONPATH (handled by scripts)

For detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

---

## Performance & Limitations

### Current Capabilities

- **Vocabulary**: 65 gesture definitions with intelligent fallbacks
- **Speed**: ~30 FPS animation (stick engine)
- **Multi-engine**: Fallback support across all 3 engines
- **Real-time**: Text-to-avatar in <1 second (stick engine)
- **Production**: Enhanced error handling, logging, validation

### Known Limitations

- **2D Visualization**: Stick engine is 2D (not 3D realistic)
- **No Facial Expressions**: Face/emotions not included
- **Limited Two-handed**: Simple two-hand coordination only
- **Simplified ASL Grammar**: Basic stopword removal, not full ASL grammar
- **No Finger Spelling**: FINGERSPELL is a placeholder, not actual letter-by-letter signing
- **Single-hand Dominant**: Most gestures emphasize one hand

### Future Roadmap

- Expand vocabulary (100+ gestures)
- Add facial expressions and head movements
- Implement proper finger spelling
- Enhanced ASL grammar rules
- Real-time webcam input
- Web-based 3D avatar (Three.js)
- Mobile app integration

---

## Additional Documentation

- **[Gesture Format Guide](docs/gesture_format.md)** - Complete JSON schema and gesture creation guide
- **[Troubleshooting](TROUBLESHOOTING.md)** - Detailed solutions for common issues
- **[Video Processing Fixes](VIDEO_PROCESSING_FIXES.md)** - YouTube integration and video handling notes
- **[Project Summary](SUMMARY.md)** - Production improvements and enhancement overview
- **[Pose Viewer](pose-viewer/README.md)** - React app for visualizing pose files
- **[Text-to-Skeleton API](text-to-skeleton/README.md)** - FastAPI service documentation

---

## Dependencies

### Core Dependencies

- **Python 3.10**
- **openai-whisper** (20250625) - Speech recognition
- **matplotlib** - 2D visualization and animation
- **ffmpeg** - Audio processing backend for Whisper

### Optional Dependencies

- **streamlit** (>=1.29.0) - Web interface
- **streamlit-audiorecorder** - Microphone input
- **moviepy** (>=1.0.3) - Video composition (human_video engine)
- **yt-dlp** (>=2024.12.13) - YouTube video downloads
- **Flask** - REST API server
- **FastAPI, uvicorn** - Skeleton service
- **spacy** - Lemmatization for skeleton engine

### Installation

```bash
# Core dependencies (included in environment.yml)
conda env create -f environment.yml

# Optional - Streamlit
pip install streamlit>=1.29.0 streamlit-audiorecorder

# Optional - Human Video
pip install moviepy>=1.0.3 yt-dlp>=2024.12.13

# Optional - APIs
pip install flask fastapi uvicorn

# Optional - Skeleton engine
pip install spacy
python -m spacy download en_core_web_sm
```

---

## Credits & Acknowledgments

- **[OpenAI Whisper](https://github.com/openai/whisper)** - State-of-the-art speech recognition
- **[WLASL Dataset](https://dxli94.github.io/WLASL/)** - World's largest video dictionary of sign language (2000+ signs)
- **ASL Linguistic Resources** - Grammar rules and gloss notation conventions
- **Matplotlib & Streamlit** - Visualization and web interface frameworks

---

## License

[License information to be added]

---

## Contributing

Contributions welcome!

**To add gestures:**
See [docs/gesture_format.md](docs/gesture_format.md) for JSON schema and examples.

**To contribute code:**

1. Fork the repository
2. Create a feature branch
3. Follow existing code patterns
4. Add tests for new features
5. Submit a pull request

For questions or discussions, please open an issue on GitHub.

---
