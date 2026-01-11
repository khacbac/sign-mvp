import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import sys
import whisper
from utils.logging_config import get_logger

logger = get_logger(__name__)


def transcribe_audio(audio_path: str, model_size: str = "medium") -> str:
    """
    Transcribes an audio file to text using Whisper.

    Args:
        audio_path (str): Path to audio file
        model_size (str): Whisper model size (tiny, base, small, medium)

    Returns:
        str: Transcribed text
    """
    logger.info("Loading Whisper model (size=%s)", model_size)
    model = whisper.load_model(model_size)

    logger.info("Transcribing audio: %s", audio_path)
    result = model.transcribe(audio_path)

    text = result["text"].strip()
    return text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Usage: python transcribe.py <audio_path>")
        sys.exit(1)

    audio_path = sys.argv[1]
    text = transcribe_audio(audio_path)

    print("\n=== TRANSCRIPTION RESULT ===")
    print(text)
