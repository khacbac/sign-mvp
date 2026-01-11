import sys
import re
from pathlib import Path
from utils.logging_config import get_logger

logger = get_logger(__name__)

# Add the project root to Python path so we can import modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def _safe_filename(text):
    """
    Sanitize text for use in filename.

    Args:
        text (str): Text to sanitize

    Returns:
        str: Safe filename string
    """
    name = text.strip().lower()
    name = re.sub(r"\s+", "_", name)
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    return name[:40] or "pose"


from asr.transcribe import transcribe_audio
from nlp.text_to_gloss import text_to_gloss
from avatar_engines.stick.loader import gesture_exists
from avatar_engines.stick.generator import generate_keypoints
from avatar_engines.stick.renderer import render_avatar
from avatar_engines.human_video import (
    create_video_loader,
    get_best_videos_with_alternatives,
    gloss_exists as wlasl_gloss_exists,
)

# Try to import compositor, handle if not available
try:
    from avatar_engines.human_video import create_compositor

    _compositor_available = True
except ImportError:
    print("Warning: Video compositor not available. Please install moviepy.")
    create_compositor = None
    _compositor_available = False

# Try to import skeleton engine
try:
    from avatar_engines.skeleton import (
        is_service_available,
        get_gloss_sequence,
        generate_pose,
        SkeletonServiceError,
    )

    _skeleton_available = True
except ImportError:
    print("Warning: Skeleton engine not available.")
    _skeleton_available = False

import matplotlib.pyplot as plt


def process_audio_to_avatar(audio_path, engine="stick"):
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
    logger.info("Processing audio: %s with engine: %s", audio_path, engine)
    print(f"Processing audio: {audio_path}")
    print(f"Using engine: {engine}")

    # Step 1: Transcribe audio to text
    print("Step 1: Transcribing audio...")
    transcription = transcribe_audio(audio_path)
    logger.info("Transcription result: %s", transcription)
    print(f"Transcription: {transcription}")

    # Step 2: Convert text to ASL gloss
    print("Step 2: Converting to ASL gloss...")
    gloss_sequence = text_to_gloss(transcription)
    logger.info("Gloss sequence: %s", gloss_sequence)
    print(f"Gloss sequence: {gloss_sequence}")

    if engine == "human_video":
        # Use WLASL video engine
        return process_with_wlasl(transcription, gloss_sequence)
    elif engine == "skeleton":
        # Use skeleton engine with FastAPI backend
        return process_with_skeleton(transcription, gloss_sequence)
    else:
        # Use stick figure engine (default)
        return process_with_stick(transcription, gloss_sequence)


def process_with_stick(transcription, gloss_sequence):
    """
    Process using stick figure avatar with improved error handling.

    Now supports fallback gestures for unknown words instead of skipping.
    """
    logger.info("Generating gesture keypoints for stick engine")
    print("Step 3: Generating gesture keypoints...")
    all_keypoints = []
    valid_glosses = []
    missing_glosses = []

    for gloss in gloss_sequence:
        # generate_keypoints now handles fallbacks internally
        keypoints = generate_keypoints(gloss, frames=30, use_fallback=True)
        all_keypoints.extend(keypoints)

        # Track which glosses we have actual gestures for vs fallbacks
        if gesture_exists(gloss):
            valid_glosses.append(gloss)
        else:
            # Using fallback gesture
            if len(gloss) <= 3:
                valid_glosses.append(f"{gloss}*")  # Mark fingerspelled
                missing_glosses.append(gloss)
            else:
                valid_glosses.append(f"{gloss}?")  # Mark unknown
                missing_glosses.append(gloss)

    logger.info(
        "Generated %d frames for %d glosses (%d using fallbacks)",
        len(all_keypoints),
        len(valid_glosses),
        len(missing_glosses),
    )
    print(f"Generated {len(all_keypoints)} frames for {len(valid_glosses)} glosses")
    if missing_glosses:
        print(
            f"Note: {len(missing_glosses)} gestures used fallback placeholders: {', '.join(missing_glosses[:5])}"
        )
        if len(missing_glosses) > 5:
            print(f"  ... and {len(missing_glosses) - 5} more")

    return transcription, gloss_sequence, all_keypoints, valid_glosses


def process_with_wlasl(transcription, gloss_sequence):
    """Process using WLASL human video avatar"""
    logger.info("Processing with WLASL human video engine")
    print("Step 3: Mapping glosses to WLASL videos...")

    # Initialize WLASL components
    loader = create_video_loader()

    # Check if compositor is available - do this after initializing components
    if not _compositor_available:
        logger.error("Video compositor not available - moviepy not installed")
        raise RuntimeError(
            "Video compositor not available. Please install moviepy: pip install moviepy"
        )

    # Map glosses to videos with alternatives for fallback
    video_candidates = []  # List of (gloss, video_options)
    valid_glosses = []
    missing_glosses = []

    for gloss in gloss_sequence:
        if wlasl_gloss_exists(gloss):
            # Get best videos with alternatives for fallback
            video_options = get_best_videos_with_alternatives(gloss, max_results=3)
            if video_options:
                video_candidates.append((gloss, video_options))
                valid_glosses.append(gloss)
            else:
                logger.warning("No video options found for gloss: %s", gloss)
                print(f"Warning: No video options found for '{gloss}', skipping...")
                missing_glosses.append(gloss)
        else:
            logger.warning("Gloss not found in WLASL dataset: %s", gloss)
            print(f"Warning: '{gloss}' not found in WLASL dataset, skipping...")
            missing_glosses.append(gloss)

    if not video_candidates:
        logger.error("No valid glosses with videos found in WLASL dataset")
        raise ValueError("No valid glosses with videos found in WLASL dataset")

    logger.info(
        "Found videos for %d glosses, skipped %d",
        len(valid_glosses),
        len(missing_glosses),
    )
    print(f"Found videos for {len(valid_glosses)} glosses")
    if missing_glosses:
        print(f"Skipped {len(missing_glosses)} missing glosses: {missing_glosses}")

    # Step 4: Download videos with fallback logic
    print("Step 4: Downloading videos...")
    video_paths = []
    downloaded_glosses = []

    for gloss, video_options in video_candidates:
        video_path = None

        # Try each video option in order of preference
        for i, video_info in enumerate(video_options):
            source = video_info.get("source", "unknown")
            video_id = video_info["video_id"]
            url = video_info["url"]

            if i == 0:
                print(f"  Downloading '{gloss}' from {source} (video_id: {video_id})")
            else:
                print(f"    Trying alternative {i+1}: {source} (video_id: {video_id})")

            video_path = loader.download_video(url, video_id)
            if video_path:
                downloaded_glosses.append(gloss)
                video_paths.append(video_path)
                break  # Success, no need to try more alternatives

        if not video_path:
            logger.warning("Failed to download any video for gloss: %s", gloss)
            print(f"  Failed to download any video for '{gloss}'")

    if not video_paths:
        logger.error("Failed to download any videos from any source")
        raise RuntimeError("Failed to download any videos from any source")

    logger.info("Successfully downloaded %d videos", len(video_paths))
    print(f"Successfully downloaded {len(video_paths)} videos")

    # Step 5: Composite videos
    print("Step 5: Compositing videos...")

    # Double-check that create_compositor is available (not None)
    if create_compositor is None:
        logger.error("Video compositor is None - moviepy not properly installed")
        raise RuntimeError(
            "Video compositor is None. Please ensure moviepy is properly installed."
        )

    compositor = create_compositor()
    output_path = compositor.composite_videos(video_paths, downloaded_glosses)

    if not output_path:
        logger.error("Failed to composite videos")
        raise RuntimeError("Failed to composite videos")

    logger.info("Created composite video: %s", output_path)
    print(f"Created composite video: {output_path}")

    return transcription, gloss_sequence, output_path, downloaded_glosses


def process_with_skeleton(transcription, gloss_sequence):
    """
    Process using skeleton avatar with FastAPI backend.

    Calls the text-to-skeleton FastAPI service to generate pose file.
    File is saved at: text-to-skeleton/output/poses/{_safe_filename(transcription)}.pose

    Returns:
        tuple: (transcription, api_gloss_sequence, None, api_gloss_sequence)
               None for result_data since no visualization in UI
    """
    logger.info("Processing with skeleton engine via FastAPI")
    print("Step 3: Generating skeleton pose via FastAPI service...")

    # Check availability
    if not _skeleton_available:
        logger.error("Skeleton engine not available - module not imported")
        raise RuntimeError("Skeleton engine not available")

    # Check service
    if not is_service_available():
        logger.error("Text-to-skeleton FastAPI service is not running")
        raise RuntimeError(
            "Text-to-skeleton FastAPI service is not running.\n\n"
            "To start the service:\n"
            "  cd text-to-skeleton\n"
            "  uvicorn main:app --reload\n\n"
            "The service should run on http://localhost:8000"
        )

    try:
        # Get gloss sequence using spaCy lemmatization
        api_gloss_sequence = get_gloss_sequence(transcription)
        logger.info("API gloss sequence: %s", api_gloss_sequence)
        print(f"API gloss sequence: {api_gloss_sequence}")

        # Generate pose file (saves to text-to-skeleton/output/poses/{_safe_filename(transcription)}.pose)
        generate_pose(transcription)
        pose_path = (
            f"text-to-skeleton/output/poses/{_safe_filename(transcription)}.pose"
        )
        logger.info("Pose file generated: %s", pose_path)
        print(f"Pose file generated successfully at: {pose_path}")

        # Return in same format as other engines
        # result_data is None since we don't visualize in UI
        return transcription, api_gloss_sequence, None, api_gloss_sequence

    except SkeletonServiceError as e:
        logger.error("Skeleton service error: %s", str(e))
        raise RuntimeError(f"Skeleton service error: {str(e)}")


def process_text_to_avatar(text, engine="stick"):
    """
    Process text directly to avatar (skip ASR step)

    Args:
        text (str): Input text to convert
        engine (str): Avatar engine to use ('stick' or 'human_video')

    Returns:
        tuple: (text, gloss_sequence, result_data, valid_glosses)
               For stick: result_data = all_keypoints
               For human_video: result_data = video_path
    """
    logger.info("Processing text: %s with engine: %s", text, engine)
    print(f"Processing text: {text}")
    print(f"Using engine: {engine}")

    # Step 1: Convert text to ASL gloss
    print("Step 1: Converting to ASL gloss...")
    gloss_sequence = text_to_gloss(text)
    logger.info("Gloss sequence: %s", gloss_sequence)
    print(f"Gloss sequence: {gloss_sequence}")

    if engine == "human_video":
        # Use WLASL video engine
        return process_with_wlasl(text, gloss_sequence)
    elif engine == "skeleton":
        # Use skeleton engine with FastAPI backend
        return process_with_skeleton(text, gloss_sequence)
    else:
        # Use stick figure engine (default)
        return process_with_stick(text, gloss_sequence)


def animate_keypoints(all_keypoints, gloss_sequence):
    """
    Animate the keypoints with gloss labels

    Args:
        all_keypoints: List of pose keypoints
        gloss_sequence: List of gloss strings
    """
    plt.figure(figsize=(4, 6))

    frames_per_gloss = (
        len(all_keypoints) // len(gloss_sequence) if gloss_sequence else 0
    )

    for i, pose in enumerate(all_keypoints):
        # Determine which gloss to show
        gloss_idx = (
            min(i // frames_per_gloss, len(gloss_sequence) - 1)
            if frames_per_gloss > 0
            else 0
        )
        current_gloss = gloss_sequence[gloss_idx] if gloss_sequence else ""

        render_avatar(pose, text=current_gloss)

    plt.show()
