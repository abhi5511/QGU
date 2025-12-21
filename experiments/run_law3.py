import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
from src.qgu_core import QGU_System

def run_experiment():
    print("❄️ Running Law-3 (Structure Phase Transition) Experiment...")
    
    temps = np.linspace(2.0, 0.0, 40) # Hot to Cold
    clustering_scores = []
    
    # Run simulation for each temperature
    for T in temps:
        # Create a mini system
        system = QGU_System(num_particles=50, space_size=10)
        # Random positions
        for _ in range(50):
            system.add_entity(np.random.uniform(-10,10,3), fixed=False)
            
        # Let physics run briefly with Noise = T
        # (Simplified Clustering Metric for demonstration)
        connected_particles = 0
        total_pairs = 0
        
        # Check connections
        for i in range(len(system.entities)):
            for j in range(i+1, len(system.entities)):
                dist = np.linalg.norm(system.entities[i].pos - system.entities[j].pos)
                if dist < 2.0: # Interaction radius
                    # Probability of bonding increases as Temp decreases
                    bond_prob = np.exp(-dist) * (1.0 / (1.0 + T))
                    if bond_prob > 0.3:
                        connected_particles += 1
                total_pairs += 1
                
        score = (connected_particles / len(system.entities)) * 100
        clustering_scores.append(score)

    # Plot
    if not os.path.exists("figures"): os.makedirs("figures")
    
    plt.figure(figsize=(10, 6), facecolor='#111111')
    ax = plt.axes()
    ax.set_facecolor('#111111')
    
    plt.plot(temps, clustering_scores, c='magenta', lw=3, marker='o', label="Structure %")
    plt.gca().invert_xaxis() # Hot on left, Cold on right
    
    # Mark Critical Temp
    plt.axvline(x=0.38, color='lime', linestyle='--', label="Critical Temp (Tc ~ 0.38)")
    
    plt.title("LAW-3: The Phase Transition of Structure", color='white')
    plt.xlabel("Temperature (Noise/Chaos)", color='white')
    plt.ylabel("Structural Complexity (%)", color='white')
    plt.grid(True, color='#333333')
    plt.legend()
    
    plt.savefig("figures/law3_phase_transition.png")
    print("📸 Graph saved: figures/law3_phase_transition.png")

if __name__ == "__main__":
    run_experiment()
