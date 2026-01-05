import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
from avatar_engines.stick.generator import generate_keypoints
from avatar_engines.stick.renderer import render_avatar

def play_sign_sequence(glosses):
    plt.figure()
    for gloss in glosses:
        frames = generate_keypoints(gloss)
        for pose in frames:
            # render_frame(pose)
            render_avatar(pose, text=gloss)
    plt.show()

if __name__ == "__main__":
    play_sign_sequence(["HELLO", "ME", "GO", "BOOK"])
