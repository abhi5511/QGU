import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import hsv_to_rgb

# --- QGU CONFIGURATION ---
BH_MASS = 5000.0      # QGU Density Mass
EVENT_HORIZON = 1.5   # Point of No Return
LIGHT_SPEED = 0.2
NUM_PHOTONS = 120     # Thodi zyada rays for better look

class Photon:
    def __init__(self, y_pos):
        self.pos = np.array([-6.0, y_pos]) # Start further back
        self.vel = np.array([LIGHT_SPEED, 0.0])
        self.history = []
        self.trapped = False
        # Start with Cyan color [Red, Green, Blue]
        self.color = np.array([0.0, 1.0, 1.0])

photons = [Photon(y) for y in np.linspace(-4, 4, NUM_PHOTONS)]

# --- VISUAL SETUP ---
fig, ax = plt.subplots(figsize=(12, 10), facecolor='black')
ax.set_facecolor('black')
ax.set_xlim(-6, 6)
ax.set_ylim(-5, 5)
ax.set_aspect('equal')
ax.axis('off')

# 1. The Event Horizon (Pure Black Void)
black_hole_circle = plt.Circle((0, 0), EVENT_HORIZON, color='black', zorder=20)
ax.add_artist(black_hole_circle)

# 2. QGU Accretion "Density Glow" (Static visual placeholder for the disk)
# Ye bas ek static orange glow hai jo high density zone ko darsha raha hai.
disk_glow = plt.Circle((0, 0), EVENT_HORIZON * 2.5, color='orange', alpha=0.15, zorder=5)
ax.add_artist(disk_glow)
disk_core_glow = plt.Circle((0, 0), EVENT_HORIZON * 1.2, color='darkred', alpha=0.3, zorder=6)
ax.add_artist(disk_core_glow)


# Lines now need individual colors, so we use LineCollection later or update individually.
# For simplicity in animation loop, we keep updating individual lines.
trails = []
for p in photons:
    # Initialize with cyan, will update in loop
    line, = ax.plot([], [], '-', color=p.color, alpha=0.8, linewidth=1.2, zorder=10)
    trails.append(line)

print("🕳️ --- QGU GARGANTUA ENGINE --- 🕳️")
print("Applying Density-based Lensing AND Redshift...")

def update(frame):
    for i, p in enumerate(photons):
        if p.trapped: continue

        # --- CORE QGU CALCS ---
        dist_vec = np.array([0.0, 0.0]) - p.pos
        dist = np.linalg.norm(dist_vec)

        if dist < EVENT_HORIZON * 0.95: # Slight buffer so lines don't hit bright edge
            p.trapped = True
            continue

        # Lensing Pull (Same as before)
        pull_strength = BH_MASS / (dist**2.5 + 0.1)
        p.vel += dist_vec * pull_strength * 0.001
        p.vel = p.vel / np.linalg.norm(p.vel) * LIGHT_SPEED
        p.pos += p.vel
        p.history.append(p.pos.copy())
        if len(p.history) > 200: p.history.pop(0)

        # --- NEW: QGU DENSITY REDSHIFT ---
        # Rule: Jitni zyada density (paas), utna zyada color shift towards Red.
        # Hum Cyan [0, 1, 1] se start kar rahe hain.
        # Orange/Red ki taraf jaane ke liye Red badhana hai, Green/Blue kam karna hai.
        
        # Density impact factor (tuned for visual look)
        density_impact = pull_strength * 0.0003

        # QGU Color shift logic:
        # Increase Red component based on density drag
        new_r = min(1.0, p.color[0] + density_impact * 3.0)
        # Decrease Green component slightly (to get yellow/orange)
        new_g = max(0.3, p.color[1] - density_impact * 1.0) 
        # Decrease Blue component rapidly (high energy fades first in QGU)
        new_b = max(0.0, p.color[2] - density_impact * 4.0)
        
        p.color = np.array([new_r, new_g, new_b])

        # Draw trail with new color
        pts = np.array(p.history)
        if len(pts) > 0:
            trails[i].set_data(pts[:, 0], pts[:, 1])
            trails[i].set_color(p.color) # Update the color of the line itself

    return trails + [black_hole_circle, disk_glow, disk_core_glow]

ani = FuncAnimation(fig, update, frames=400, interval=20, blit=True)
plt.title("QGU Gargantua: Density Lensing & Redshift", color='orange')
plt.show()
