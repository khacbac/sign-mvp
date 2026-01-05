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
import matplotlib.pyplot as plt

def process_audio_to_avatar(audio_path):
    """
    Complete pipeline: Audio → Text → Gloss → Avatar Animation

    Args:
        audio_path (str): Path to the audio file

    Returns:
        tuple: (transcription, gloss_sequence, all_keypoints, valid_glosses)
    """
    print(f"Processing audio: {audio_path}")

    # Step 1: Transcribe audio to text
    print("Step 1: Transcribing audio...")
    transcription = transcribe_audio(audio_path)
    print(f"Transcription: {transcription}")

    # Step 2: Convert text to ASL gloss
    print("Step 2: Converting to ASL gloss...")
    gloss_sequence = text_to_gloss(transcription)
    print(f"Gloss sequence: {gloss_sequence}")

    # Step 3: Generate keypoints for each gloss
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
