import os
import sys
from pathlib import Path

# Add the project root to Python path so we can import modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from asr.transcribe import transcribe_audio
from nlp.text_to_gloss import text_to_gloss
from avatar_engines.stick.loader import gesture_exists
from avatar_engines.stick.generator import generate_keypoints
from avatar_engines.stick.renderer import render_avatar
from avatar_engines.human_video import (
    get_gloss_mapper,
    create_video_loader,
    gloss_exists as wlasl_gloss_exists
)

# Try to import compositor, handle if not available
try:
    from avatar_engines.human_video import create_compositor
    _compositor_available = True
except ImportError:
    print("Warning: Video compositor not available. Please install moviepy.")
    create_compositor = None
    _compositor_available = False

import matplotlib.pyplot as plt

def process_audio_to_avatar(audio_path, engine='stick'):
    """
    Complete pipeline: Audio → Text → Gloss → Avatar Animation

    Args:
        audio_path (str): Path to the audio file
        engine (str): Avatar engine to use ('stick' or 'human_video')

    Returns:
        tuple: (transcription, gloss_sequence, result_data, valid_glosses)
               For stick: result_data = all_keypoints
               For human_video: result_data = video_path
    """
    print(f"Processing audio: {audio_path}")
    print(f"Using engine: {engine}")

    # Step 1: Transcribe audio to text
    print("Step 1: Transcribing audio...")
    transcription = transcribe_audio(audio_path)
    print(f"Transcription: {transcription}")

    # Step 2: Convert text to ASL gloss
    print("Step 2: Converting to ASL gloss...")
    gloss_sequence = text_to_gloss(transcription)
    print(f"Gloss sequence: {gloss_sequence}")

    if engine == 'human_video':
        # Use WLASL video engine
        return process_with_wlasl(transcription, gloss_sequence)
    else:
        # Use stick figure engine (default)
        return process_with_stick(transcription, gloss_sequence)

def process_with_stick(transcription, gloss_sequence):
    """Process using stick figure avatar"""
    print("Step 3: Generating gesture keypoints...")
    all_keypoints = []
    valid_glosses = []

    for gloss in gloss_sequence:
        if gesture_exists(gloss):
            keypoints = generate_keypoints(gloss)
            all_keypoints.extend(keypoints)
            valid_glosses.append(gloss)
        else:
            print(f"Warning: No gesture found for '{gloss}', skipping...")

    print(f"Generated {len(all_keypoints)} frames for {len(valid_glosses)} valid glosses")
    return transcription, gloss_sequence, all_keypoints, valid_glosses

def process_with_wlasl(transcription, gloss_sequence):
    """Process using WLASL human video avatar"""
    print("Step 3: Mapping glosses to WLASL videos...")

    # Check if compositor is available
    if not _compositor_available:
        raise RuntimeError("Video compositor not available. Please install moviepy: pip install moviepy")

    # Initialize WLASL components
    mapper = get_gloss_mapper()
    loader = create_video_loader()
    compositor = create_compositor()

    # Map glosses to videos
    video_metadata = []
    valid_glosses = []
    missing_glosses = []

    for gloss in gloss_sequence:
        if wlasl_gloss_exists(gloss):
            best_video = mapper.get_best_video(gloss)
            video_metadata.append(best_video)
            valid_glosses.append(gloss)
        else:
            print(f"Warning: '{gloss}' not found in WLASL dataset, skipping...")
            missing_glosses.append(gloss)

    if not video_metadata:
        raise ValueError("No valid glosses found in WLASL dataset")

    print(f"Found {len(video_metadata)} videos for {len(valid_glosses)} glosses")

    # Step 4: Download videos
    print("Step 4: Downloading videos...")
    video_paths = []

    for i, video_info in enumerate(video_metadata):
        gloss = valid_glosses[i]
        print(f"  Downloading '{gloss}' (video_id: {video_info['video_id']})")

        video_path = loader.download_video(video_info['url'], video_info['video_id'])
        if video_path:
            video_paths.append(video_path)
        else:
            print(f"  Failed to download video for '{gloss}'")

    if not video_paths:
        raise RuntimeError("Failed to download any videos")

    # Step 5: Composite videos
    print("Step 5: Compositing videos...")
    output_path = compositor.composite_videos(video_paths, valid_glosses)

    if not output_path:
        raise RuntimeError("Failed to composite videos")

    print(f"Created composite video: {output_path}")

    return transcription, gloss_sequence, output_path, valid_glosses

def process_text_to_avatar(text):
    """
    Process text directly to avatar (skip ASR step)

    Args:
        text (str): Input text to convert

    Returns:
        tuple: (text, gloss_sequence, all_keypoints, valid_glosses)
    """
    print(f"Processing text: {text}")

    # Step 1: Convert text to ASL gloss
    print("Step 1: Converting to ASL gloss...")
    gloss_sequence = text_to_gloss(text)
    print(f"Gloss sequence: {gloss_sequence}")

    # Step 2: Generate keypoints for each gloss
    print("Step 2: Generating gesture keypoints...")
    all_keypoints = []
    valid_glosses = []

    for gloss in gloss_sequence:
        if gesture_exists(gloss):
            keypoints = generate_keypoints(gloss)
            all_keypoints.extend(keypoints)
            valid_glosses.append(gloss)
        else:
            print(f"Warning: No gesture found for '{gloss}', skipping...")

    print(f"Generated {len(all_keypoints)} frames for {len(valid_glosses)} valid glosses")

    return text, gloss_sequence, all_keypoints, valid_glosses

def animate_keypoints(all_keypoints, gloss_sequence):
    """
    Animate the keypoints with gloss labels

    Args:
        all_keypoints: List of pose keypoints
        gloss_sequence: List of gloss strings
    """
    plt.figure(figsize=(4, 6))

    frames_per_gloss = len(all_keypoints) // len(gloss_sequence) if gloss_sequence else 0

    for i, pose in enumerate(all_keypoints):
        # Determine which gloss to show
        gloss_idx = min(i // frames_per_gloss, len(gloss_sequence) - 1) if frames_per_gloss > 0 else 0
        current_gloss = gloss_sequence[gloss_idx] if gloss_sequence else ""

        render_avatar(pose, text=current_gloss)

    plt.show()
