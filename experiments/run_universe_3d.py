import sys
import os
# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from src.qgu_core import QGU_System

def run_3d_simulation():
    print("🌌 Initializing QGU Universe in 3D...")
    
    # 1. Setup 3D System (Bada Space)
    system = QGU_System(space_size=30)
    
    # Create a Central Star Cluster (Heavy Density)
    for _ in range(100):
        # Gaussian Cloud in center
        pos = np.random.normal(0, 3, 3) 
        system.add_entity(pos, mass=2.0, fixed=True)
        
    # Create Orbiting Planets/Particles
    print("✨ Spawning particles in 3D space...")
    for i in range(60):
        # Random positions in a shell
        pos = np.random.uniform(-20, 20, 3)
        p = system.add_entity(pos, mass=1.0, fixed=False)
        
        # Initial Physics: Give them velocity tangent to center (Orbit)
        # Cross product ensures perpendicular velocity
        center_vec = np.array([0,0,0]) - pos
        p.vel = np.cross(center_vec, [0, 0, 1]) * 0.02
        # Add random drift
        p.vel += np.random.uniform(-0.05, 0.05, 3)

    # 2. Visualization Setup
    plt.ion() # Interactive mode
    fig = plt.figure(figsize=(12, 10), facecolor='black')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    
    # Remove ugly grid/axes for Space look
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.axis('off')

    print("🎥 3D Simulation Started... (Press Ctrl+C to stop)")

    # 3. Simulation Loop
    try:
        for t in range(1000):
            # Physics Step (Reusing Core Logic implicitly)
            for p in system.entities:
                if p.fixed: continue
                
                # Simple 3D Gravity Calculation
                force = np.zeros(3)
                for other in system.entities:
                    if p == other: continue
                    delta = other.pos - p.pos
                    dist = np.linalg.norm(delta) + 1.0 # Softening
                    
                    # F = G * m1 * m2 / r^2
                    f_mag = (0.8 * p.mass * other.mass) / (dist**2)
                    force += f_mag * (delta/dist)
                
                p.acc = force / p.mass
                p.vel += p.acc * 0.1
                p.pos += p.vel * 0.1
                
                # Boundary Wrap (Torus Universe)
                for i in range(3):
                    if p.pos[i] > 30: p.pos[i] = -30
                    if p.pos[i] < -30: p.pos[i] = 30
            
            # Rendering
            ax.cla()
            ax.set_xlim(-25, 25)
            ax.set_ylim(-25, 25)
            ax.set_zlim(-25, 25)
            ax.axis('off')
            
            # Extract Data for Plotting
            xs = [e.pos[0] for e in system.entities]
            ys = [e.pos[1] for e in system.entities]
            zs = [e.pos[2] for e in system.entities]
            
            # Gold for Core, Cyan for Particles
            colors = ['#FFD700' if e.fixed else '#00FFFF' for e in system.entities]
            sizes = [30 if e.fixed else 10 for e in system.entities]
            alpha = [0.6 if e.fixed else 0.9 for e in system.entities]
            
            ax.scatter(xs, ys, zs, c=colors, s=sizes, alpha=alpha, depthshade=True)
            
            # Cinematic Camera Rotation
            ax.view_init(elev=20, azim=t*0.5)
            
            plt.title(f"QGU 3D Simulation | Frame: {t}", color='white')
            plt.draw()
            plt.pause(0.001) # Fast render

    except KeyboardInterrupt:
        print("\n🛑 Simulation Stopped.")
        plt.close()

    plt.show(block=True)

if __name__ == "__main__":
    run_3d_simulation()