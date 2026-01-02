# Streamlit UI Implementation Plan

## Overview
Create a Streamlit web interface with three input options for the sign language translation system:
1. **Local Audio Buttons** - Quick test playback of existing audio files
2. **Upload Audio** - User file upload functionality
3. **Microphone Input** - Real-time speech recording

## Current State
- Command-line interface only (`main.py`, `demo_with_text.py`)
- Existing audio files in `input/` directory
- Whisper-based ASR pipeline already implemented
- Avatar rendering with matplotlib

## Implementation Plan

### 1. Create Streamlit App Structure
**Files to create:**
- `app.py` - Main Streamlit application

### 2. Implement Input Methods

#### Option 1: Local Audio Buttons
- Scan the `input/` directory for audio files
- Create clickable buttons for each audio file
- Play audio preview within Streamlit
- "Translate" button to process selected audio

#### Option 2: Upload Audio
- Use `st.file_uploader()` for audio file upload
- Support formats: WAV, MP3, M4A, etc.
- Save uploaded file to temporary location
- Process with existing pipeline

#### Option 3: Microphone Input
- Use `st.audio()` with `start_button` for recording
- Record audio via browser's Web Audio API
- Save as temporary WAV file
- Requires additional dependencies: `streamlit-audiorecorder`

### 3. Integration Strategy
- Modify existing pipeline functions to work without command-line args
- Create modular functions that can be called from Streamlit
- Separate audio processing logic from UI

### 4. UI/UX Considerations
- Loading states during processing
- Progress indicators for long operations
- Error handling and user feedback
- Auto-play of avatar animation after processing
- Display transcription and gloss steps

### 5. Dependencies to Add
- `streamlit`
- `streamlit-audiorecorder` (for microphone)
- Update `environment.yml`

### 6. Refactoring Needed
- Extract audio processing logic from `main.py` into reusable functions
- Create pipeline module: `pipeline/process_audio.py`
- Ensure matplotlib rendering works in Streamlit context

## Key Files to Modify

### New Files:
- `app.py` - Main Streamlit application
- `pipeline/process_audio.py` - Extracted processing logic

### Modified Files:
- `main.py` - Refactor to use pipeline module
- `environment.yml` - Add Streamlit dependencies

### Unchanged Files:
- `asr/transcribe.py` - ASR module remains as-is
- `nlp/text_to_gloss.py` - NLP processing unchanged
- `signs/` - Gesture definitions and rendering remain same

## Testing Strategy
1. Test each input method individually
2. Verify all three audio files work with local buttons
3. Test file upload with various formats
4. Test microphone recording and processing
5. Verify avatar animation displays correctly in Streamlit

## Next Steps
1. Create pipeline module by refactoring main.py
2. Build basic Streamlit app with local audio buttons
3. Add upload functionality
4. Add microphone recording capability
5. Polish UI with status indicators and error handling