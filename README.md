# Citadel Map Coordinate Extraction Tool

## 📌 Description
This project extracts boundary coordinate points from a real map image
to build a realistic simulation environment.

The user clicks along the boundary of the map, and the tool generates
NumPy coordinate points that can be reused in another simulation file.

## 🗺️ How It Works
1. The map image is displayed (vertically flipped for correct alignment)
2. User clicks along the boundary starting from the entrance
3. Press ENTER to finish
4. Coordinates are printed and copied into `citadel_walker.py`

## 📂 Files
- `boundary_point_picker.py` : Main tool for extracting points
- `citadel_map.png` : Map image
- `citadel_walker.py` : Simulation file that uses the points

## ▶️ How to Run
```bash
python boundary_point_picker.py
