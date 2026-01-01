import matplotlib.pyplot as plt

# Skeleton connections
ARMS = [
    ("LEFT_SHOULDER", "LEFT_ELBOW", "LEFT_WRIST"),
    ("RIGHT_SHOULDER", "RIGHT_ELBOW", "RIGHT_WRIST"),
]

def draw_circle(x, y, r=0.03, color="black"):
    circle = plt.Circle((x, y), r, color=color, fill=True)
    plt.gca().add_patch(circle)

def draw_limb(a, b, width=6, color="black"):
    plt.plot([a[0], b[0]], [a[1], b[1]],
             linewidth=width, color=color, solid_capstyle="round")

def render_avatar(pose):
    plt.clf()

    # --------------------
    # Head
    # --------------------
    head_x = 0.5
    head_y = 0.3
    draw_circle(head_x, head_y, r=0.05)

    # --------------------
    # Body
    # --------------------
    body_top = (0.5, 0.35)
    body_bottom = (0.5, 0.55)
    draw_limb(body_top, body_bottom, width=8)

    # --------------------
    # Arms
    # --------------------
    for shoulder, elbow, wrist in ARMS:
        draw_limb(pose[shoulder], pose[elbow], width=6)
        draw_limb(pose[elbow], pose[wrist], width=6)

        # Hand
        draw_circle(pose[wrist][0], pose[wrist][1], r=0.025)

    # --------------------
    # Canvas settings
    # --------------------
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().invert_yaxis()
    plt.axis("off")
    plt.pause(0.03)
