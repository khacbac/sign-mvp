import argparse
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from pipeline.process_audio import process_audio_to_avatar, animate_keypoints

def main():
    parser = argparse.ArgumentParser(description='Sign Language Translation Pipeline')
    parser.add_argument('audio_file', type=str, help='Path to the audio file')
    args = parser.parse_args()

    # Process the audio
    transcription, gloss_sequence, all_keypoints, valid_glosses = process_audio_to_avatar(args.audio_file)

    # Display results
    print("\n" + "="*50)
    print("TRANSLATION COMPLETE")
    print("="*50)
    print(f"\nTranscription: {transcription}")
    print(f"ASL Gloss: {' '.join(gloss_sequence)}")
    print(f"\nValid signs: {len(valid_glosses)}")
    print("="*50)

    # Show the avatar animation
    print("\nStarting avatar animation...")
    animate_keypoints(all_keypoints, valid_glosses)

    print("Animation complete!")

if __name__ == "__main__":
    main()
