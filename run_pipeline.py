import sys
import os

# Phase 1: ASR
from asr.transcribe import transcribe_audio

# Phase 2: Text → Gloss
from nlp.text_to_gloss import text_to_gloss

# Phase 4: Rendering
from renderer.play_sign_sequence import play_gloss_sequence

def main():
    if len(sys.argv) < 2:
        print("Usage: python run_pipeline.py <audio_file>")
        sys.exit(1)

    audio_path = sys.argv[1]

    if not os.path.exists(audio_path):
        print(f"[ERROR] Audio file not found: {audio_path}")
        sys.exit(1)

    print("\n[Phase 1] Transcribing audio...")
    text = transcribe_audio(audio_path)
    print(f"[ASR OUTPUT] {text}")

    print("\n[Phase 2] Converting text to gloss...")
    gloss_list = text_to_gloss(text)
    print(f"[GLOSS OUTPUT] {gloss_list}")

    print("\n[Phase 4] Rendering sign language...")
    play_gloss_sequence(gloss_list)

if __name__ == "__main__":
    main()