import cv2
import json
import os
import sys


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAPPING_PATH = os.path.join(BASE_DIR, "mapping", "gloss_to_video.json")
VIDEO_DIR = os.path.join(BASE_DIR, "signs", "videos")

with open(MAPPING_PATH, "r", encoding="utf-8") as f:
    GLOSS_TO_VIDEO = json.load(f)

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"[ERROR] Cannot open video: {video_path}")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Sign Language Output", frame)

        # Press 'q' to stop playback early
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

    cap.release()

def play_gloss_sequence(gloss_list):
    for gloss in gloss_list:
        gloss = gloss.upper()

        if gloss not in GLOSS_TO_VIDEO:
            print(f"[WARNING] No video found for gloss: {gloss}")
            continue

        video_file = GLOSS_TO_VIDEO[gloss]
        video_path = os.path.join(VIDEO_DIR, video_file)

        print(f"[INFO] Playing sign for: {gloss}")
        play_video(video_path)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Example gloss input (temporary for Phase 4 testing)
    test_gloss = ["I", "WANT", "WATER"]

    play_gloss_sequence(test_gloss)
