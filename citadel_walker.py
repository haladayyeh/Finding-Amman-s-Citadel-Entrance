"""
Citadel Walker Simulation
Finding Amman's Citadel Entrance using a Biased Random Walk

This is a beginner-friendly simulation that shows a walker trying
to find the entrance to Amman's Citadel by walking along the street
perimeter and deciding which direction to go at each step.

Authors: Hala Dayyeh, Sondos Awad.
Date: December 2025
sub: computer application lab.
"""

"""
(very important)!!
we worked on two things in this project:
first,moving on the original map using real points on it
second:moving using a random path.
u can edit on STREET_TYPE = 'random' to change the path .
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.interpolate import interp1d #extra library for the points path.

# -----------------------------
# Simulation parameters
# -----------------------------
PERIMETER_LENGTH = 200
STEP_SIZE = 1
ALPHA = 0.025
TOLERANCE = 0.5
START_POSITION = PERIMETER_LENGTH / 2
FORCED_STEPS = 10

# Global variables for smooth street coordinates
smooth_x = None
smooth_y = None
interp_x = None
interp_y = None

# Choose street path type:'points' or 'random'.
STREET_TYPE = 'random'  # Change to 'points' to use predefined coordinates
# -----------------------------
# Street contour setup
# -----------------------------

# METHOD 1 (random)
def create_street_contour_random():
    """
    Returns X,Y coordinates of the street perimeter with smooth interpolation.
    Creates a random irregular closed path using sinusoidal functions.
    """
    theta = np.linspace(0, 2 * np.pi, 500)

    base_radius = 300
    r = (
        base_radius
        + 50 * np.sin(3 * theta)
        + 30 * np.cos(5 * theta)
        + 20 * np.sin(7 * theta)
        + 15 * np.cos(2 * theta)
        + 10 * np.sin(9 * theta)
    )

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    return x, y

#METHOD 2 (points)
def create_street_contour_by_points():
    """
    Returns X,Y coordinates of the street perimeter with smooth interpolation.
    *** These points are extracted from predefined coordinates covering the perimeter. ***
    From file (getting points.py)
    """
    points = np.array([
        [460.95, 253.64], [409.23, 252.33], [376.50, 269.36], [351.62, 283.76], [322.82, 306.02],
        [297.28, 336.13], [276.33, 373.45], [266.51, 405.53], [242.29, 433.68], [209.56, 463.14],
        [172.90, 488.02], [132.96, 504.38], [94.99, 518.13], [54.40, 526.64], [22.32, 531.22],
        [19.05, 499.80], [23.63, 442.19], [24.94, 402.25], [34.76, 356.43], [43.93, 321.07],
        [53.09, 279.18], [59.64, 237.28], [64.88, 194.07], [85.82, 165.92], [106.77, 128.60],
        [129.69, 93.90], [153.26, 58.55], [180.75, 34.33], [213.49, 16.65], [265.20, 11.42],
        [301.87, 9.45], [332.64, 25.16], [358.17, 45.46], [387.63, 70.34], [421.02, 91.94],
        [473.39, 105.69], [509.40, 103.72], [542.78, 102.41], [584.03, 110.27], [624.62, 120.09],
        [661.28, 125.33], [694.01, 136.46], [739.84, 139.73], [785.67, 146.28], [817.09, 148.90],
        [855.06, 156.10], [874.70, 160.68], [908.74, 165.92], [931.00, 175.74], [932.97, 198.65],
        [910.71, 207.16], [881.25, 201.27], [833.46, 193.41], [795.49, 199.96], [744.42, 205.20],
        [697.94, 218.95], [686.16, 270.01], [645.57, 307.33], [579.45, 287.69], [510.05, 268.70],
        [464.88, 255.61]
    ])

    points = points - points.mean(axis=0)
    x = points[:, 0]
    y = points[:, 1]

    x = np.append(x, x[0])
    y = np.append(y, y[0])

    t = np.linspace(0, 1, len(x))
    t_smooth = np.linspace(0, 1, 500)
    x_smooth = interp1d(t, x, kind='cubic')(t_smooth)
    y_smooth = interp1d(t, y, kind='cubic')(t_smooth)

    return x_smooth, y_smooth


def create_street_contour():
    """
    Main function to get street path based on STREET_TYPE setting.
    """
    if STREET_TYPE == 'points':
        return create_street_contour_by_points()
    return create_street_contour_random()

# -----------------------------
# Direction & probability
# -----------------------------
def d_right(pos):
    """Distance to entrance if going right (counter-clockwise)"""
    return (PERIMETER_LENGTH - pos) % PERIMETER_LENGTH

def d_left(pos):
    """Distance to entrance if going left (clockwise)"""
    return pos % PERIMETER_LENGTH

def prob_right(pos):
    """Compute probability to move right based on distance to entrance"""

    left = d_left(pos)
    right = d_right(pos)

    # When right path is shorter, probability increases
    exp = -ALPHA * (left - right)
    return 1.0 / (1.0 + np.exp(exp))

# -----------------------------
# Street coordinate helpers
# -----------------------------
def setup_street():
    """Prepare global smooth_x and smooth_y for easy coordinate lookup"""
    global smooth_x, smooth_y, interp_x, interp_y
    smooth_x, smooth_y = create_street_contour()
    t = np.linspace(0, 1, len(smooth_x))

    # Use cubic interpolation for points, linear for random
    kind = 'cubic' if STREET_TYPE == 'points' else 'linear'
    interp_x = interp1d(t, smooth_x, kind=kind)
    interp_y = interp1d(t, smooth_y, kind=kind)

def get_street_position(perimeter_pos):
    """Convert perimeter position (0-L) to X,Y coordinates"""
    t = (perimeter_pos / PERIMETER_LENGTH) % 1.0
    return float(interp_x(t)), float(interp_y(t))

# -----------------------------
# Random walk simulation
# -----------------------------
def run_simulation(force_direction=None):
    """
    Simulate walker until entrance is reached.
    force_direction: 'left' or 'right' for first FORCED_STEPS
    """
    positions = [START_POSITION] # list of positions
    probabilities = [prob_right(START_POSITION)] # list of probabilities
    current = START_POSITION
    step = 0

    while True:
        step += 1
        p = prob_right(current)

        if step <= FORCED_STEPS and force_direction is not None:
            go_right = (force_direction == 'right')
        else:
            go_right = np.random.random() < p

        current = (current + STEP_SIZE) % PERIMETER_LENGTH if go_right else (current - STEP_SIZE) % PERIMETER_LENGTH
        positions.append(current)
        probabilities.append(prob_right(current))

        # Stop when entrance is reached (within tolerance ϵ)
        if abs(current) < TOLERANCE or abs(current - PERIMETER_LENGTH) < TOLERANCE:
            break

    return positions, probabilities

# -----------------------------
# Animation
# -----------------------------
def animate_walk():
    """
    Create and display animated dual-plot visualization of two walker simulations.
    Left plot shows walker position on street, right plot shows probability evolution.
    """
    setup_street()

    # Run two simulations with different forced starting directions
    np.random.seed(42)
    pos1, prob1 = run_simulation(force_direction='left')
    np.random.seed(43)
    pos2, prob2 = run_simulation(force_direction='right')

    # Convert perimeter positions to X,Y coordinates for visualization
    coords1 = [get_street_position(p) for p in pos1]
    coords2 = [get_street_position(p) for p in pos2]
    entrance_x, entrance_y = get_street_position(0)


    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("Finding Amman's Citadel Entrance ", fontsize=14, fontweight='bold')

    # Setup left plot: Street map with walker
    ax1.plot(smooth_x, smooth_y, 'k-', linewidth=3, label='Perimeter Road')
    ax1.plot(entrance_x, entrance_y, 'r*', markersize=20, label='Main Entrance', zorder=5, markeredgecolor='black', markeredgewidth=1)
    ax1.set_aspect('equal')
    ax1.set_xlabel('X Coordinate')
    ax1.set_ylabel('Y Coordinate')
    ax1.set_title('Walker Position on Street')
    ax1.grid(True, alpha=0.3)
    ax1.legend()


    walker, = ax1.plot([], [], 'ro', markersize=10, zorder=4)
    trail, = ax1.plot([], [], 'b-', alpha=0.3, linewidth=1.5)

    # Setup right plot: Probability evolution
    ax2.set_xlim(0, len(pos1) + len(pos2))
    ax2.set_ylim(0, 1)
    ax2.axhline(0.5, color='black', linestyle='--', alpha=0.5)
    ax2.set_xlabel('Step Number')
    ax2.set_ylabel('Probability of Going Counter-clockwise')
    ax2.set_title('Probability Evolution')
    ax2.grid(True, alpha=0.3)


    prob_line, = ax2.plot([], [], 'b-', linewidth=2)

    # Add text boxes for simulation info
    sim_text = ax1.text(0.40, 0.98, '', transform=ax1.transAxes, verticalalignment='top', fontsize=8, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    step_text = ax1.text(0.40, 0.88, '', transform=ax1.transAxes, verticalalignment='top', fontsize=8, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

    def update(frame):
        """
        Update function called for each animation frame.
        Updates walker position, trail, and probability plot for both simulations.
        """

        if frame < len(pos1):
            # First simulation (clockwise start)
            sim_num = 1
            idx = frame
            x_data = [c[0] for c in coords1[:idx+1]]
            y_data = [c[1] for c in coords1[:idx+1]]
            prob_x = list(range(idx+1))
            prob_y = prob1[:idx+1]
            direction = "Clockwise"
        else:
            # Second simulation (counter-clockwise start)
            sim_num = 2
            idx = frame - len(pos1)
            x_data = [c[0] for c in coords2[:idx+1]]
            y_data = [c[1] for c in coords2[:idx+1]]
            prob_x = list(range(len(pos1), len(pos1)+idx+1))
            prob_y = prob2[:idx+1]
            direction = "Counter-clockwise"

        # Update walker position and trail
        walker.set_data([x_data[-1]], [y_data[-1]])
        trail.set_data(x_data, y_data)

        # Update probability line
        prob_line.set_data(prob_x, prob_y)


        sim_text.set_text(f'Simulation {sim_num}\nForced Start: {direction}')
        step_text.set_text(f'Step: {idx + 1}')


        if frame == len(pos1) - 1:
            ax2.axvline(x=len(pos1), color='black', linestyle='--', linewidth=2, alpha=0.7, label='Simulation 2 Start')
            ax2.legend()

        return walker, trail, prob_line, sim_text, step_text


    total_frames = len(pos1) + len(pos2)
    anim = FuncAnimation(fig, update, frames=total_frames, interval=50, blit=True, repeat=True)
    plt.tight_layout()
    plt.show()


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    print("🏛️ Citadel Walker Simulation")
    print(f"Street Type: {STREET_TYPE.upper()}")
    print(f"Perimeter Length: {PERIMETER_LENGTH}")
    print(f"Step Size: {STEP_SIZE}")
    print(f"Reliability (alpha): {ALPHA}")
    print(f"Start Position: {START_POSITION}")
    print(f"Forced Steps: {FORCED_STEPS}")
    print("\nTip: Change STREET_TYPE to 'points' or 'random' to switch street path")

    animate_walk()
