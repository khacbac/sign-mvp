from signs.gestures import GESTURE_MAP

def generate_keypoints(gloss, frames=30):
    gesture = GESTURE_MAP.get(gloss, GESTURE_MAP["IDLE"])
    sequence = []

    for f in range(frames):
        pose = gesture(f, frames)
        sequence.append(pose)

    return sequence
