# Human Video Avatar Engine - Flow Documentation

## Overview

The human video avatar engine converts sign language glosses into a composited video using real sign language videos from the WLASL dataset. This document explains the complete flow from input to output.

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Human Video Avatar Engine                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐    │
│  │ GlossMapper  │───▶│ VideoLoader  │───▶│VideoCompositor│    │
│  │              │    │              │    │              │    │
│  │ Maps glosses │    │ Downloads &  │    │ Composites   │    │
│  │ to video IDs │    │ caches videos│    │ into single  │    │
│  └──────────────┘    └──────────────┘    └──────────────┘    │
│         │                   │                      │          │
│         │                   │                      │          │
│         ▼                   ▼                      ▼          │
│  ┌──────────────────────────────────────────────────────┐    │
│  │         WLASL_v0.3.json (Metadata)                   │    │
│  │         cache/ (Downloaded Videos)                  │    │
│  └──────────────────────────────────────────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Complete Flow

### Step 1: Initialization

```
User Input (Audio/Text)
    ↓
Pipeline: process_audio_to_avatar(engine='human_video')
    ↓
process_with_wlasl()
```

**What happens:**

- Audio is transcribed to text (if audio input)
- Text is converted to gloss sequence (e.g., ["HELLO", "I", "LOVE", "YOU"])
- Engine components are initialized:
  - `GlossMapper`: Loads WLASL metadata (2000+ glosses, 21,000+ videos)
  - `VideoLoader`: Sets up cache directory
  - `VideoCompositor`: Initialized if moviepy is available

### Step 2: Gloss Mapping

```
Gloss Sequence: ["HELLO", "I", "LOVE", "YOU"]
    ↓
For each gloss:
    ↓
GlossMapper.get_best_videos_with_alternatives(gloss, max_results=3)
    ↓
Returns: List of video metadata sorted by source preference
```

**What happens:**

1. **GlossMapper** looks up each gloss in the WLASL metadata
2. For each gloss, it finds all available videos
3. Videos are sorted by source preference:
   - `signschool` (highest priority)
   - `asldeafined`
   - `valencia-asl`
   - `startasl`
   - `handspeak`
   - ... (10 total preferred sources)
4. Returns top 3 video options per gloss for fallback

**Example:**

```python
gloss = "HELLO"
video_options = [
    {
        'video_id': '12345',
        'source': 'signschool',
        'url': 'https://...',
        'signer_id': '001',
        ...
    },
    {
        'video_id': '67890',
        'source': 'asldeafined',
        'url': 'https://...',
        ...
    },
    # ... more alternatives
]
```

### Step 3: Video Download (with Fallback)

```
For each gloss with video options:
    ↓
Try video option 1 (preferred source)
    ↓
VideoLoader.download_video(url, video_id)
    ↓
Check cache first → If cached, return path
    ↓
If not cached:
    - Check if YouTube URL → Use yt-dlp
    - Otherwise → HTTP download with requests
    ↓
Save to cache/ directory
    ↓
If download fails → Try next alternative
```

**What happens:**

1. **VideoLoader** checks if video is already cached
2. If cached, returns cached path immediately
3. If not cached:
   - Checks cache size (max 10GB), cleans up if needed
   - Determines if URL is YouTube or direct HTTP
   - Downloads video:
     - **YouTube**: Uses `yt-dlp` library
     - **HTTP**: Uses `requests` with streaming
   - Saves to `cache/{video_id}.mp4`
   - Returns path to cached video
4. If download fails, tries next alternative video
5. If all alternatives fail, skips that gloss

**Cache Management:**

- Videos cached in `avatar_engines/human_video/cache/`
- Max cache size: 10GB (configurable)
- Automatic cleanup of oldest videos when limit approached
- Cache checked before every download

### Step 4: Video Composition

```
List of downloaded video paths
    ↓
VideoCompositor.composite_videos(video_paths, glosses)
    ↓
For each video:
    - Load with VideoFileClip
    - Resize to 1280x720 (if needed)
    - Set FPS to 25 (if needed)
    ↓
Concatenate all clips
    ↓
Write to output file (temp directory)
    ↓
Return output path
```

**What happens:**

1. **VideoCompositor** loads each video file
2. Normalizes all videos:
   - Resize to 1280x720 (720p)
   - Set FPS to 25
   - Handle both MoviePy 1.x and 2.x compatibility
3. Concatenates videos in sequence
4. Writes final composite video to temp directory
5. Filename includes glosses: `wlasl_HELLO_I_LOVE_YOU_20240101_120000.mp4`
6. Returns path to final video

**Output Settings:**

- Resolution: 1280x720 (720p)
- FPS: 25
- Codec: libx264
- Audio: None (sign language videos typically don't have audio)
- Format: MP4

### Step 5: Return to Application

```
Output video path
    ↓
Returned to Streamlit app
    ↓
Displayed in modal dialog
    ↓
User can view and download
```

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
│ GlossMapper                         │
│ - Lookup "HELLO" → video_id: 12345  │
│ - Lookup "I" → video_id: 23456      │
│ - Lookup "LOVE" → video_id: 34567    │
│ - Lookup "YOU" → video_id: 45678    │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ VideoLoader                         │
│ - Check cache for 12345             │
│ - Download if missing               │
│ - Save to cache/12345.mp4           │
│ - Repeat for each video_id          │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│ VideoCompositor                     │
│ - Load cache/12345.mp4              │
│ - Load cache/23456.mp4              │
│ - Load cache/34567.mp4              │
│ - Load cache/45678.mp4              │
│ - Resize & normalize                │
│ - Concatenate                       │
│ - Write to temp/wlasl_*.mp4        │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────┐
│ Final Video │
└─────────────┘
```

## Component Details

### GlossMapper (`gloss_mapper.py`)

- **Purpose**: Maps gloss strings to video metadata
- **Data Source**: `WLASL_v0.3.json` (11MB, 2000+ glosses)
- **Key Methods**:
  - `get_best_video(gloss)`: Returns single best video
  - `get_best_videos_with_alternatives(gloss, max_results)`: Returns multiple options
  - `gloss_exists(gloss)`: Check if gloss is in dataset
- **Performance**: O(1) lookup using hash map

### VideoLoader (`video_loader.py`)

- **Purpose**: Downloads and caches videos
- **Features**:
  - Automatic caching (10GB limit)
  - YouTube support via yt-dlp
  - HTTP download with retries
  - Cache cleanup when full
- **Key Methods**:
  - `download_video(url, video_id)`: Download and cache
  - `is_cached(video_id)`: Check cache
  - `get_cache_info()`: Get cache statistics

### VideoCompositor (`video_compositor.py`)

- **Purpose**: Combines multiple videos into one
- **Dependencies**: moviepy (1.x or 2.x)
- **Features**:
  - Video normalization (size, FPS)
  - Concatenation
  - Progress tracking
  - Error handling
- **Key Methods**:
  - `composite_videos(video_paths, glosses)`: Create composite video

## Error Handling & Fallbacks

1. **Missing Gloss**:

   - Gloss not in WLASL → Skipped, warning logged
   - Similar glosses can be found with `find_similar_glosses()`

2. **Download Failures**:

   - Primary video fails → Try alternative #1
   - Alternative #1 fails → Try alternative #2
   - All alternatives fail → Skip gloss, continue with others

3. **Cache Issues**:

   - Cache full → Automatic cleanup of oldest videos
   - Download fails → Retry with exponential backoff (3 attempts)

4. **Composition Failures**:
   - Video file corrupted → Skip that video, continue
   - All videos fail → Raise error

## Performance Characteristics

- **Gloss lookup**: O(1) - Instant
- **Metadata loading**: ~1 second (one-time, cached)
- **Video download**: 2-5 seconds per video (first time)
- **Cached video access**: <0.1 seconds
- **Video composition**: 5-10 seconds for typical sequence

## Integration Points

### With Pipeline (`pipeline/process_audio.py`)

```python
def process_with_wlasl(transcription, gloss_sequence):
    # Step 1: Initialize components
    mapper = get_gloss_mapper()
    loader = create_video_loader()
    compositor = create_compositor()

    # Step 2: Map glosses to videos
    # Step 3: Download videos
    # Step 4: Composite videos
    # Step 5: Return output path
```

### With Streamlit (`app.py`)

```python
# User selects "human_video" engine
result = process_audio_to_avatar(audio_path, engine='human_video')
transcription, gloss_sequence, video_path, valid_glosses = result

# Display video in modal
show_results_dialog(..., video_path=video_path)
```

## Configuration

All settings in `config.py`:

- **Cache**: `VIDEO_CACHE_DIR`, `MAX_CACHE_SIZE_GB`
- **Download**: `MAX_RETRIES`, `TIMEOUT_SECONDS`, `CHUNK_SIZE`
- **Video Quality**: `PREFERRED_SOURCES` (ordered list)
- **Output**: `OUTPUT_VIDEO_WIDTH`, `OUTPUT_VIDEO_HEIGHT`, `OUTPUT_FPS`

## Example Execution

```python
# Input
glosses = ["HELLO", "WORLD"]

# Step 1: Map
mapper = get_gloss_mapper()
videos = [mapper.get_best_video(g) for g in glosses]
# Returns: [{'video_id': '12345', 'url': '...', ...}, ...]

# Step 2: Download
loader = create_video_loader()
paths = [loader.download_video(v['url'], v['video_id']) for v in videos]
# Returns: [Path('cache/12345.mp4'), Path('cache/67890.mp4')]

# Step 3: Composite
compositor = create_compositor()
output = compositor.composite_videos(paths, glosses)
# Returns: Path('temp/wlasl_HELLO_WORLD_20240101_120000.mp4')
```

## Summary

The human video avatar engine provides a complete pipeline from gloss sequences to composited sign language videos:

1. **GlossMapper** → Finds videos for each gloss
2. **VideoLoader** → Downloads and caches videos
3. **VideoCompositor** → Combines videos into final output

All components work together seamlessly with automatic fallbacks, caching, and error handling to provide a robust sign language video generation system.
