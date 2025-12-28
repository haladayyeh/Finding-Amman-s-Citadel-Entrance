# Finding Amman’s Citadel Entrance  
### Citadel Map Coordinate Extraction Tool

## 📌 Overview
This project is a Python-based tool designed to extract accurate boundary
coordinate points from a real map image to build a realistic
simulation environment.  
The extracted coordinates support simulations analyzing movement and navigation
toward the entrance of **Amman’s Citadel**.

---

## 🎯 Project Objectives
- Convert real-world map boundaries into usable coordinate data
- Enable accurate simulation and analysis of spatial movement
- Provide a simple interactive tool for manual boundary selection
- Support further simulation logic in a separate walker module

---

## 🗺️ How the Tool Works
1. A map image is loaded and vertically flipped to ensure correct coordinate alignment.
2. The user clicks sequentially along the boundary, starting from the entrance.
3. Each click records a coordinate point.
4. The selected boundary is visualized in real time.
5. Pressing **ENTER** finalizes the selection.
6. The tool outputs NumPy-formatted coordinates ready for reuse.

---

## 📂 Project Structure
├── getting_points.py # Interactive tool for extracting boundary coordinates
├── citadel_map.png # Map image of Amman’s Citadel
├── citadel_walker.py # Simulation file that uses the extracted points
├── README.md # Project documentation
└── .gitignore # Ignored system files

---

## 🧑‍🤝‍🧑 Team Members
- **Hala Dayyeh**
- **Sondos Awwad**

