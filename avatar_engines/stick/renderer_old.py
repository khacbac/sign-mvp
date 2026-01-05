import matplotlib.pyplot as plt

EDGES = [
    ("LEFT_SHOULDER", "LEFT_ELBOW"),
    ("LEFT_ELBOW", "LEFT_WRIST"),
    ("RIGHT_SHOULDER", "RIGHT_ELBOW"),
    ("RIGHT_ELBOW", "RIGHT_WRIST"),
]

def render_frame(pose):
    plt.clf()

    for a, b in EDGES:
        x = [pose[a][0], pose[b][0]]
        y = [pose[a][1], pose[b][1]]
        plt.plot(x, y, marker="o")

    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().invert_yaxis()
    plt.pause(0.03)
