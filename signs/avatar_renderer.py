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

def render_avatar(pose, text=None):
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
    # Text Display
    # --------------------
    if text:
        plt.text(0.5, 0.85, text,
                ha='center', va='center',
                fontsize=16, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8))

    # --------------------
    # Canvas settings
    # --------------------
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().invert_yaxis()
    plt.axis("off")
    plt.pause(0.03)

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def render_avatar_streamlit(placeholder, pose, text=None):
    """
    Render avatar in a Streamlit placeholder

    Args:
        placeholder: Streamlit empty placeholder (st.empty())
        pose: Dict of pose keypoints
        text: Optional text to display
    """
    # Create super compact figure with minimal margins
    fig, ax = plt.subplots(figsize=(1.8, 2.5))
    fig.subplots_adjust(left=0, right=1, top=0.95, bottom=0.05)  # Minimize margins
    ax.set_xlim(0, 1)
    ax.set_ylim(0.25, 0.8)  # Adjusted viewport
    ax.invert_yaxis()
    ax.axis('off')

    # --------------------
    # Head
    # --------------------
    head_x = 0.5
    head_y = 0.3
    circle = plt.Circle((head_x, head_y), 0.05, color='black', fill=True)
    ax.add_patch(circle)

    # --------------------
    # Body (shortened)
    # --------------------
    body_top = (0.5, 0.35)
    body_bottom = (0.5, 0.5)
    ax.plot([body_top[0], body_bottom[0]], [body_top[1], body_bottom[1]],
            linewidth=6, color='black', solid_capstyle='round')

    # --------------------
    # Arms
    # --------------------
    for shoulder, elbow, wrist in ARMS:
        # Draw arm segments
        ax.plot([pose[shoulder][0], pose[elbow][0]],
                [pose[shoulder][1], pose[elbow][1]],
                linewidth=4, color='black', solid_capstyle='round')
        ax.plot([pose[elbow][0], pose[wrist][0]],
                [pose[elbow][1], pose[wrist][1]],
                linewidth=4, color='black', solid_capstyle='round')

        # Hand
        hand_circle = plt.Circle((pose[wrist][0], pose[wrist][1]), 0.02,
                               color='black', fill=True)
        ax.add_patch(hand_circle)

    # --------------------
    # Text Display (compact)
    # --------------------
    if text:
        # Very compact text above head, small font, no box
        ax.text(0.5, 0.2, text,
                ha='center', va='center',
                fontsize=8,  # Small font
                fontweight='normal')  # Normal weight to be less prominent

    # Display in placeholder
    placeholder.pyplot(fig)
    plt.close(fig)
