import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os

def run_helix_proof():
    print("🧬 INITIALIZING DNA FLOW TEST...")
    print("   Testing: Why does Nature choose a Helix over a Ladder?")

    # --- SIMULATION PARAMETERS ---
    n_layers = 20          # Number of base pairs
    radius = 1.0           # Width of DNA
    vertical_spacing = 0.8 # Distance between layers (Rise)
    
    # We will sweep the twist angle from 0 (Ladder) to 180 degrees
    test_angles = np.linspace(0, 100, 100)
    stability_scores = []

    # QGU Interaction Function (Modified for flow shadowing)
    # If atoms are directly on top of each other (Angle 0), Repulsion is HIGH.
    # If they are staggered (Angle > 0), Repulsion drops.
    def calculate_interlayer_stress(angle_deg):
        angle_rad = np.deg2rad(angle_deg)
        stress = 0
        
        # Simulate interaction between Layer i and Layer i+1
        # In QGU, flow travels vertically. 
        # Max Stress = Perfectly Aligned (0 degree difference)
        # Min Stress = Perfectly Staggered (Optimized Flow)
        
        # We model stress as a function of the 'overlap' between stacked bases.
        # Simple heuristic: Stress drops as molecules move away from "eclipsed" position.
        # But we also need 'cohesion' (they can't be too far apart radially).
        
        # Let's look at the distance between Strand A(i) and Strand A(i+1)
        # Pos A(i)   = [r, 0, 0]
        # Pos A(i+1) = [r*cos(theta), r*sin(theta), h]
        
        dx = radius * (1 - np.cos(angle_rad))
        dy = radius * (np.sin(angle_rad))
        dz = vertical_spacing
        
        dist_sq = dx**2 + dy**2 + dz**2
        distance = np.sqrt(dist_sq)
        
        # Lennard-Jones style potential for vertical neighbors
        # They want to be close (connected), but not eclipsed.
        # Ideally, there is a "sweet spot" distance.
        
        # Repulsion term (Avoid overlap/shadowing)
        repulsion = 1.0 / (distance**12) 
        # Attraction term (Chemical bonding/Flow continuity)
        attraction = 1.0 / (distance**6)
        
        energy = repulsion - attraction
        return energy

    # --- RUN SWEEP ---
    for theta in test_angles:
        score = calculate_interlayer_stress(theta)
        stability_scores.append(score)

    # --- FIND OPTIMUM ---
    min_energy = min(stability_scores)
    optimal_angle = test_angles[stability_scores.index(min_energy)]

    # --- VISUALIZATION ---
    fig = plt.figure(figsize=(14, 6), facecolor='#111111')
    
    # Plot 1: The Stability Curve
    ax1 = fig.add_subplot(1, 2, 1, facecolor='#111111')
    ax1.plot(test_angles, stability_scores, color='cyan', linewidth=3)
    
    # Mark Ladder (0 deg)
    ladder_score = stability_scores[0]
    ax1.scatter([0], [ladder_score], color='red', s=100, zorder=5, label="Straight Ladder (0°)")
    ax1.text(5, ladder_score, "UNSTABLE\n(High Flow Shadow)", color='red', verticalalignment='bottom')
    
    # Mark Helix (Optimum)
    ax1.scatter([optimal_angle], [min_energy], color='magenta', s=150, zorder=5, label=f"Optimal Helix ({optimal_angle:.1f}°)")
    ax1.text(optimal_angle, min_energy - 0.05, "STABLE DNA\n(Perfect Stacking)", color='magenta', 
             horizontalalignment='center', verticalalignment='top', fontweight='bold')
    
    ax1.set_title("QGU STABILITY ANALYSIS: TWIST ANGLE", color='white')
    ax1.set_xlabel("Twist Angle (Degrees)", color='white')
    ax1.set_ylabel("Flow Stress / Energy", color='white')
    ax1.grid(True, color='#333333')
    ax1.legend()
    ax1.tick_params(colors='white')

    # Plot 2: 3D Structure of the Winner
    ax2 = fig.add_subplot(1, 2, 2, projection='3d', facecolor='#111111')
    ax2.set_facecolor('#111111')
    
    # Generate Optimal Helix
    z = np.linspace(0, n_layers * vertical_spacing, n_layers)
    theta = np.deg2rad(optimal_angle) * np.arange(n_layers)
    x1 = radius * np.cos(theta)
    y1 = radius * np.sin(theta)
    x2 = radius * np.cos(theta + np.pi) # Opposite strand
    y2 = radius * np.sin(theta + np.pi)
    
    # Draw Strands
    ax2.plot(x1, y1, z, color='lime', linewidth=4, alpha=0.8, label="Flow Strand A")
    ax2.plot(x2, y2, z, color='lime', linewidth=4, alpha=0.8, label="Flow Strand B")
    
    # Draw Base Pairs (Rungs)
    for i in range(n_layers):
        ax2.plot([x1[i], x2[i]], [y1[i], y2[i]], [z[i], z[i]], color='white', alpha=0.5)
        
    ax2.set_title(f"EMERGENT STRUCTURE\n(Twist = {optimal_angle:.1f}°)", color='white')
    ax2.axis('off')

    plt.tight_layout()
    
    # Save
    if not os.path.exists("figures"): os.makedirs("figures")
    save_path = "figures/qgu_dna_proof.png"
    plt.savefig(save_path, facecolor='#111111')
    print(f"📸 DNA Proof Generated: {save_path}")
    print(f"   Optimum Twist Found: {optimal_angle:.2f} degrees")
    plt.show()

if __name__ == "__main__":
    run_helix_proof()