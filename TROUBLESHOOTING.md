# Troubleshooting Guide

## Common Issues and Solutions

### 1. Streamlit Error: "module 'streamlit' has no attribute 'dialog'"

**Status**: ✅ **FIXED** - The app now uses `st.expander` instead of `st.dialog`

**What happened**:
The `st.dialog` decorator had module caching issues when used inside nested functions in Streamlit's hot-reload environment.

**Solution Applied**:
Replaced `st.dialog` with `st.expander` in `app.py:72`. The expander provides similar functionality (collapsible results view) without the caching issues.

**If you still see this error**:
```bash
# Clear all caches
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete

# Restart Streamlit
streamlit run app.py
```

**Note**: The app now uses `st.expander("🤟 Translation Results", expanded=True)` which provides a better, more reliable user experience than modal dialogs.

### 2. Import Errors After Updates

If you see import errors after making changes:

```bash
# Clear all caches
rm -rf __pycache__
rm -rf avatar_engines/__pycache__
rm -rf avatar_engines/stick/__pycache__
rm -rf nlp/__pycache__
rm -rf pipeline/__pycache__

# Restart your application
```

### 3. Unknown Gesture Warnings

**Expected Behavior**: When you use words not in the vocabulary, you'll see:
```
Note: 2 gestures used fallback placeholders: COMPUTER, TECHNOLOGY
```

This is **normal** and **intentional**. The system uses:
- `FINGERSPELL` gesture for short unknown words (≤3 chars)
- `UNKNOWN` gesture for longer unknown words
- These words are marked with `*` or `?` in the output

**To Fix**: Add more gesture JSON files to `avatar_engines/stick/gestures/json/`

### 4. Long Text Processing Slow

**Cause**: Processing very long text (>100 words) can be slow

**Solutions**:
```python
# Reduce max chunk size
from nlp.text_to_gloss import text_to_gloss
glosses = text_to_gloss(long_text, chunk=True, max_chunk_words=10)

# Or disable chunking for short texts
glosses = text_to_gloss(text, chunk=False)
```

### 5. Diagnostic Warnings in IDE

If you see warnings like "variable not accessed", these have been fixed:
- Unused imports removed from `process_audio.py`
- Unused parameters in `generator.py` prefixed with `_`

To verify all diagnostics are clean:
```bash
# If using basedpyright/pylance
python -m basedpyright .
```

### 6. Testing the Improvements

Run the comprehensive test suite:
```bash
python test_improvements.py
```

Expected output:
```
✓ Your stick avatar engine is production-ready!
✓ 65 gestures available (51 → 65, +27%)
✓ Fallback mechanisms working
✓ Long text chunking enabled
✓ Input validation active
✓ Enhanced synonym mapping (60+ mappings)
```

### 7. WLASL Video Engine Errors

If you get "Video compositor not available":

```bash
pip install moviepy
```

### 8. Performance Issues

#### Memory Issues
If processing very long audio files:
```python
# Use smaller Whisper model
from asr.transcribe import transcribe_audio
text = transcribe_audio(audio_path, model_size="tiny")  # Instead of "base"
```

#### Animation Rendering Slow
```python
# Reduce frames per gesture
from avatar_engines.stick.generator import generate_keypoints
keypoints = generate_keypoints(gloss, frames=20)  # Instead of 30
```

## Checking System Health

### Quick Health Check
```bash
python -c "
from nlp.text_to_gloss import text_to_gloss, validate_input
from avatar_engines.stick.generator import generate_keypoints
from avatar_engines.stick.loader import gesture_exists
import os

# Check gesture count
gesture_dir = 'avatar_engines/stick/gestures/json'
count = len([f for f in os.listdir(gesture_dir) if f.endswith('.json')])
print(f'Gestures: {count}')

# Check fallbacks exist
print(f'UNKNOWN exists: {gesture_exists(\"UNKNOWN\")}')
print(f'FINGERSPELL exists: {gesture_exists(\"FINGERSPELL\")}')

# Test processing
glosses = text_to_gloss('Hello world')
print(f'NLP working: {len(glosses) > 0}')

# Test generation
frames = generate_keypoints('HELLO', frames=10)
print(f'Generation working: {len(frames) == 10}')
"
```

Expected output:
```
Gestures: 65
UNKNOWN exists: True
FINGERSPELL exists: True
NLP working: True
Generation working: True
```

## Getting Help

### Enable Debug Logging
```python
import logging
logging.basicConfig(level=logging.INFO)

# Now run your code - you'll see detailed logs
```

### Report Issues

If you encounter a bug:

1. Check this troubleshooting guide
2. Clear all caches
3. Verify environment with health check above
4. Check PRODUCTION_IMPROVEMENTS.md for details on changes
5. Run test_improvements.py to identify the issue

### Reverting Changes

If you need to disable any improvement:

**Disable Fallback Gestures**:
```python
from avatar_engines.stick.generator import generate_keypoints
keypoints = generate_keypoints(gloss, use_fallback=False)
```

**Disable Text Chunking**:
```python
from nlp.text_to_gloss import text_to_gloss
glosses = text_to_gloss(text, chunk=False)
```

**Skip Input Validation**:
```python
from nlp.text_to_gloss import _process_text_to_gloss
glosses = _process_text_to_gloss(text)  # Direct processing without validation
```

## Common Command Reference

```bash
# Start Streamlit app
streamlit run app.py

# Test improvements
python test_improvements.py

# Test NLP only
python nlp/text_to_gloss.py

# Test transcription
python asr/transcribe.py input/audio.wav

# Clear all caches
find . -type d -name "__pycache__" -exec rm -r {} +

# Count gestures
ls avatar_engines/stick/gestures/json/*.json | wc -l
```
