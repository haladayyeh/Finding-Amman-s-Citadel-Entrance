"""
====================================================================
Image Coordinate Extraction Tool for Map Points
====================================================================
Purpose:
    Extract coordinate points from a real map image to create
    a more realistic simulation environment.

Instructions:
    1. The map image is saved as: citadel_map.png
    2. Execute this script - the map image will display
    3. Click to mark boundary points starting from the entrance
    4. Press ENTER when finished
    5. Copy the generated coordinates
    6. Paste into: citadel_walker.py

Note: Image is displayed FLIPPED for correct coordinate alignment.

by: Hala Dayyeh, Sondos Awwad
====================================================================
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

class BoundaryPointPicker:
    def __init__(self, image_path):
        self.points = []
        self.fig, self.ax = plt.subplots(figsize=(12, 8))

        try:
            self.img = mpimg.imread(image_path)
            self.img = np.flipud(self.img)  # Flip vertically

            self.ax.imshow(self.img)
            self.ax.set_title('Click along the boundary (Start from entrance) | Press ENTER when done',
                              fontsize=12, fontweight='bold')

            # Connect events
            self.fig.canvas.mpl_connect('button_press_event', self.onclick)
            self.fig.canvas.mpl_connect('key_press_event', self.onkey)

            plt.tight_layout()
            plt.show()

        except FileNotFoundError:
            print("ERROR: Could not find 'citadel_map.png'")

    def onclick(self, event):
        if event.inaxes != self.ax:
            return

        x, y = event.xdata, event.ydata
        self.points.append((x, y))

        # Plot point
        self.ax.plot(x, y, 'ro', markersize=8)

        # Draw connecting line
        if len(self.points) > 1:
            xs = [p[0] for p in self.points]
            ys = [p[1] for p in self.points]
            self.ax.plot(xs, ys, 'r-', linewidth=2, alpha=0.7)

        self.fig.canvas.draw()
        print(f"Point {len(self.points)}: ({x:.1f}, {y:.1f})")

    def onkey(self, event):
        if event.key == 'enter':
            plt.close()
            self.print_results()

    def print_results(self):
        if len(self.points) < 3:
            print("\nERROR: Need at least 3 points")
            return

        print("\n" + "="*60)
        print(f"Total points: {len(self.points)}")
        print("\nCopy this into citadel_walker.py:\n")
        print("boundary_points = np.array([")

        for i, (x, y) in enumerate(self.points):
            comma = "," if i < len(self.points) - 1 else ""
            print(f"    [{x:.2f}, {y:.2f}]{comma}")

        print("])")
        print("="*60)


if __name__ == "__main__":
    print("Starting Boundary Point Picker...")
    print("Instructions: Click points starting from entrance, then press ENTER\n")
    picker = BoundaryPointPicker('citadel_map.png')
