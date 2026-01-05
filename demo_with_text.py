#!/usr/bin/env python3
"""
Demo: Avatar rendering with text labels
Shows the current gesture name below the avatar during animation
"""

import matplotlib.pyplot as plt
from avatar_engines.stick.generator import generate_keypoints
from avatar_engines.stick.renderer import render_avatar

def demo_with_text():
    # Demo sequence: "HELLO ME LOVE YOU"
    glosses = ["HELLO", "ME", "LOVE", "YOU"]

    print("Starting avatar animation with text labels...")
    print(f"Sequence: {' '.join(glosses)}")
    print("\nClose the window to exit.")

    plt.figure(figsize=(4, 6))

    for gloss in glosses:
        print(f"Signing: {gloss}")
        frames = generate_keypoints(gloss)
        for pose in frames:
            render_avatar(pose, text=gloss)

    plt.show()

if __name__ == "__main__":
    demo_with_text()
