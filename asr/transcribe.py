import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import sys
import whisper


def transcribe_audio(audio_path: str, model_size: str = "medium") -> str:
    """
    Transcribes an audio file to text using Whisper.

    Args:
        audio_path (str): Path to audio file
        model_size (str): Whisper model size (tiny, base, small, medium)

    Returns:
        str: Transcribed text
    """
    print("[INFO] Loading Whisper model...")
    model = whisper.load_model(model_size)

    print(f"[INFO] Transcribing audio: {audio_path}")
    result = model.transcribe(audio_path)

    text = result["text"].strip()
    return text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <audio_path>")
        sys.exit(1)

    audio_path = sys.argv[1]
    text = transcribe_audio(audio_path)

    print("\n=== TRANSCRIPTION RESULT ===")
    print(text)
