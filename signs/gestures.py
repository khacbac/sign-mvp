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

# === NEW GESTURES (38 additions) ===

# Static Gestures
def mother(frame, total):
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.52, 0.36)  # Hand at chin
    return pose

def father(frame, total):
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.52, 0.32)  # Hand at forehead
    return pose

def he(frame, total):  # Also works for SHE
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.65, 0.45)  # Point diagonal
    return pose

def they(frame, total):
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.65, 0.45)  # Point sweep position
    return pose

def look(frame, total):
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.6, 0.35)  # Point forward
    return pose

# Linear Motion Gestures
def food(frame, total):
    t = frame / total
    pose = base_pose()
    y_motion = 0.45 - 0.15 * t  # Move to mouth
    pose["RIGHT_WRIST"] = (0.5, y_motion)
    return pose

def good(frame, total):
    t = frame / total
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.5 + 0.1 * t, 0.35 + 0.05 * t)  # Forward from chin
    return pose

def bad(frame, total):
    t = frame / total
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.5 + 0.15 * t, 0.35 + 0.05 * t)  # Away from chin
    return pose

def know(frame, total):
    t = frame / total
    pose = base_pose()
    if t < 0.3:
        progress = t / 0.3
        pose["RIGHT_WRIST"] = (0.55 + 0.05 * progress, 0.4 - 0.08 * progress)
    else:
        pose["RIGHT_WRIST"] = (0.6, 0.32)  # Temple
    return pose

def give(frame, total):
    t = frame / total
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.5 + 0.15 * t, 0.4)  # Forward push
    return pose

def take(frame, total):
    t = frame / total
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.65 - 0.15 * t, 0.4)  # Pull toward
    return pose

def come(frame, total):
    t = frame / total
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.6 - 0.1 * t, 0.4)  # Beckoning
    return pose

def learn(frame, total):
    t = frame / total
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.5 + 0.05 * t, 0.45 - 0.13 * t)  # To forehead
    return pose

def see(frame, total):
    t = frame / total
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.52 + 0.08 * t, 0.32 + 0.03 * t)  # V from eyes
    return pose

def tomorrow(frame, total):
    t = frame / total
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.55 + 0.07 * t, 0.35)  # Forward from cheek
    return pose

def yesterday(frame, total):
    t = frame / total
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.55 - 0.07 * t, 0.35)  # Backward from cheek
    return pose

def why(frame, total):
    t = frame / total
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.52 + 0.06 * t, 0.32 + 0.03 * t)  # Forehead pull
    return pose

def need(frame, total):
    t = frame / total
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.5, 0.4 + 0.1 * t)  # Down motion
    return pose

# Oscillatory/Wave Gestures
def what(frame, total):
    t = frame / total
    shake = 0.04 * math.sin(4 * math.pi * t)
    pose = base_pose()
    pose["LEFT_WRIST"] = (0.45 + shake, 0.4)
    pose["RIGHT_WRIST"] = (0.55 + shake, 0.4)
    return pose

def where(frame, total):
    t = frame / total
    shake = 0.05 * math.sin(3 * math.pi * t)
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.6 + shake, 0.4)
    return pose

def name(frame, total):
    t = frame / total
    tap = 0.02 * abs(math.sin(2 * math.pi * t))
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.52, 0.35 - tap)
    return pose

# Circular/Arc Motion Gestures
def please(frame, total):
    t = frame / total
    angle = 2 * math.pi * t
    radius = 0.03
    center = (0.52, 0.45)
    pose = base_pose()
    pose["RIGHT_WRIST"] = (
        center[0] + radius * math.cos(angle),
        center[1] + radius * math.sin(angle)
    )
    return pose

def sorry(frame, total):
    t = frame / total
    angle = 2 * math.pi * t
    radius = 0.04
    center = (0.52, 0.45)
    pose = base_pose()
    pose["RIGHT_WRIST"] = (
        center[0] + radius * math.cos(angle),
        center[1] + radius * math.sin(angle)
    )
    return pose

def we(frame, total):
    t = frame / total
    angle = math.pi * t  # Semicircle
    radius = 0.08
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.45 + radius * (1 - math.cos(angle)), 0.45)
    return pose

def when(frame, total):
    t = frame / total
    if t < 0.5:
        angle = 4 * math.pi * t
        radius = 0.02
        pose = base_pose()
        pose["RIGHT_WRIST"] = (0.52 + radius * math.cos(angle), 0.35 + radius * math.sin(angle))
    else:
        pose = base_pose()
        pose["RIGHT_WRIST"] = (0.6, 0.4)
    return pose

def day(frame, total):
    t = frame / total
    angle = math.pi * t
    radius = 0.1
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.5 + radius * math.cos(angle), 0.35 - radius * 0.3 * math.sin(angle))
    return pose

def who(frame, total):
    t = frame / total
    angle = 2 * math.pi * t
    radius = 0.02
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.52 + radius * math.cos(angle), 0.36 + radius * math.sin(angle))
    return pose

# Tapping/Repetitive Gestures
def work(frame, total):
    tap = 0.02 * (frame % 8) / 8
    pose = base_pose()
    pose["LEFT_WRIST"] = (0.45, 0.45)
    pose["RIGHT_WRIST"] = (0.47, 0.45 - tap)
    return pose

def time(frame, total):
    tap = 0.02 * (frame % 8) / 8
    pose = base_pose()
    pose["LEFT_WRIST"] = (0.45, 0.45)
    pose["RIGHT_WRIST"] = (0.45 - tap, 0.45)
    return pose

def eat(frame, total):
    tap = 0.03 * (frame % 6) / 6
    pose = base_pose()
    pose["RIGHT_WRIST"] = (0.5, 0.32 + tap)
    return pose

def more(frame, total):
    t = frame / total
    tap = 0.03 * math.sin(math.pi * 2 * t)
    pose = base_pose()
    pose["LEFT_WRIST"] = (0.48, 0.4 + tap)
    pose["RIGHT_WRIST"] = (0.52, 0.4 - tap)
    return pose

# Two-Hand Symmetric Gestures
def home(frame, total):
    t = frame / total
    pose = base_pose()
    if t < 0.5:
        progress = t * 2
        pose["LEFT_WRIST"] = (0.45, 0.4 - 0.05 * progress)
        pose["RIGHT_WRIST"] = (0.55, 0.4 - 0.05 * progress)
    else:
        progress = (t - 0.5) * 2
        pose["LEFT_WRIST"] = (0.45 - 0.03 * progress, 0.35)
        pose["RIGHT_WRIST"] = (0.55 + 0.03 * progress, 0.35)
    return pose

def school(frame, total):
    t = frame / total
    clap = 0.1 * abs(math.sin(math.pi * t))
    pose = base_pose()
    pose["LEFT_WRIST"] = (0.5 - clap, 0.4)
    pose["RIGHT_WRIST"] = (0.5 + clap, 0.4)
    return pose

def have(frame, total):
    t = frame / total
    spread = 0.1 * (1 - t)
    pose = base_pose()
    pose["LEFT_WRIST"] = (0.5 - spread, 0.45)
    pose["RIGHT_WRIST"] = (0.5 + spread, 0.45)
    return pose

def friend(frame, total):
    t = frame / total
    pose = base_pose()
    if t < 0.5:
        progress = t * 2
        pose["LEFT_WRIST"] = (0.45, 0.4)
        pose["RIGHT_WRIST"] = (0.55 - 0.05 * progress, 0.4)
    else:
        progress = (t - 0.5) * 2
        pose["LEFT_WRIST"] = (0.45 + 0.05 * progress, 0.4)
        pose["RIGHT_WRIST"] = (0.5, 0.4)
    return pose

def now(frame, total):
    t = frame / total
    drop = 0.1 * t
    pose = base_pose()
    pose["LEFT_WRIST"] = (0.45, 0.4 + drop)
    pose["RIGHT_WRIST"] = (0.55, 0.4 + drop)
    return pose

def finish(frame, total):
    t = frame / total
    spread = 0.1 * t
    pose = base_pose()
    pose["LEFT_WRIST"] = (0.5 - 0.05 - spread, 0.4 + 0.05 * t)
    pose["RIGHT_WRIST"] = (0.5 + 0.05 + spread, 0.4 + 0.05 * t)
    return pose

def help(frame, total):
    t = frame / total
    lift = 0.1 * t
    pose = base_pose()
    pose["LEFT_WRIST"] = (0.45, 0.45 - lift)
    pose["RIGHT_WRIST"] = (0.45, 0.5 - lift)
    return pose

def love(frame, total):
    t = frame / total
    pose = base_pose()
    # Cross arms over chest (hugging motion)
    if t < 0.4:
        # Open arms
        progress = t / 0.4
        pose["LEFT_WRIST"] = (0.45 - 0.05 * progress, 0.4 + 0.05 * progress)
        pose["RIGHT_WRIST"] = (0.55 + 0.05 * progress, 0.4 + 0.05 * progress)
    else:
        # Cross over chest
        progress = (t - 0.4) / 0.6
        pose["LEFT_WRIST"] = (0.4 + 0.15 * progress, 0.45)
        pose["RIGHT_WRIST"] = (0.6 - 0.15 * progress, 0.45)
    return pose

GESTURE_MAP = {
    # Existing 12 gestures
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
    "FOOD": food,
    "EAT": eat,
    "GOOD": good,
    "BAD": bad,
    "MORE": more,
    "PLEASE": please,
    "SORRY": sorry,
    "HELP": help,
    "HAVE": have,
    "NEED": need,
    "KNOW": know,
    "SEE": see,
    "LOOK": look,
    "LEARN": learn,
    "GIVE": give,
    "TAKE": take,
    "COME": come,
    "HOME": home,
    "SCHOOL": school,
    "WORK": work,
    "TIME": time,
    "MOTHER": mother,
    "FATHER": father,
    "FRIEND": friend,
    "HE": he,
    "SHE": he,  # Same gesture as HE
    "WE": we,
    "THEY": they,
    "WHO": who,
    "NAME": name,
    "WHAT": what,
    "WHERE": where,
    "WHEN": when,
    "WHY": why,
    "NOW": now,
    "TOMORROW": tomorrow,
    "YESTERDAY": yesterday,
    "FINISH": finish,
    "DAY": day,
    "LOVE": love,
}
