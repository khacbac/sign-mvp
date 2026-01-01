import sys
import matplotlib.pyplot as plt

from asr.transcribe import transcribe_audio
from nlp.text_to_gloss import text_to_gloss
from signs.generator import generate_keypoints
from signs.avatar_renderer import render_avatar

def play_sign_sequence(glosses):
    plt.figure(figsize=(4, 6))

    for gloss in glosses:
        frames = generate_keypoints(gloss)
        for pose in frames:
            render_avatar(pose, text=gloss)

    plt.show()

def main(audio_path):
    print("[1] Transcribing audio...")
    text = transcribe_audio(audio_path)
    print("  → Text:", text)

    print("[2] Converting text to gloss...")
    glosses = text_to_gloss(text)
    print("  → Glosses:", glosses)

    print("[3] Rendering avatar...")
    play_sign_sequence(glosses)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py input/audio.wav")
        sys.exit(1)

    main(sys.argv[1])
