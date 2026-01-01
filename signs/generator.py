from signs.gestures import GESTURE_MAP

def generate_keypoints(gloss, frames=30):
    if gloss not in GESTURE_MAP:
        print(f"[WARN] No gesture for '{gloss}', using IDLE")
    gesture = GESTURE_MAP.get(gloss, GESTURE_MAP["IDLE"])
    sequence = []

    for f in range(frames):
        pose = gesture(f, frames)
        sequence.append(pose)

    return sequence
