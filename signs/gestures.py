import math

def idle(frame, total):
    return base_pose()

def hello(frame, total):
    t = frame / total
    wave = 0.05 * math.sin(2 * math.pi * 2 * t)
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.6 + wave, 0.4)
    return pose

def thank_you(frame, total):
    t = frame / total
    move = 0.1 * t
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.55, 0.45 - move)
    return pose

def yes(frame, total):
    t = frame / total
    nod = 0.03 * math.sin(2 * math.pi * t)
    pose = base_pose()
    pose["RIGHT_ELBOW"] = (0.55, 0.45 + nod)
    return pose

def no(frame, total):
    t = frame / total
    shake = 0.05 * math.sin(2 * math.pi * t)
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.6 + shake, 0.4)
    return pose

def me(frame, total):
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.5, 0.55)
    return pose

def you(frame, total):
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.7, 0.45)
    return pose

def go(frame, total):
    t = frame / total
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.5 + 0.2 * t, 0.45)
    return pose

def stop(frame, total):
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.6, 0.35)
    return pose

def book(frame, total):
    t = frame / total
    spread = 0.05 * math.sin(math.pi * t)
    pose = base_pose()
    pose["LEFT_WRIST"] = (0.45 - spread, 0.45)
    pose["RIGHT_WRIST"] = (0.55 + spread, 0.45)
    return pose

def base_pose():
    return {
        "LEFT_SHOULDER": (0.45, 0.5),
        "LEFT_ELBOW": (0.45, 0.45),
        "LEFT_WRIST": (0.45, 0.4),
        "RIGHT_SHOULDER": (0.55, 0.5),
        "RIGHT_ELBOW": (0.55, 0.45),
        "RIGHT_WRIST": (0.55, 0.4),
    }

def want(frame, total):
    t = frame / total
    pull = 0.05 * (1 - t)
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.55 - pull, 0.45)
    return pose

def water(frame, total):
    t = frame / total
    tap = 0.02 * (frame % 5)
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.6, 0.45 + tap)
    return pose

GESTURE_MAP = {
    "IDLE": idle,
    "HELLO": hello,
    "THANK-YOU": thank_you,
    "YES": yes,
    "NO": no,
    "ME": me,
    "YOU": you,
    "GO": go,
    "STOP": stop,
    "BOOK": book,
    "WANT": want,
    "WATER": water,
}
