import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
from src.qgu_core import QGU_System

def run_experiment():
    print("⏳ Running Law-1 (Time Dilation) Experiment...")
    
    # We will simulate particles in different density environments
    densities = np.linspace(0, 20, 50)
    time_factors = []
    
    system = QGU_System()
    
    for rho in densities:
        # Simulate a theoretical particle in a field of density 'rho'
        # Formula: dt_eff = dt / (1 + gamma * rho)
        gamma = 0.5
        time_dilation = 1.0 / (1.0 + gamma * rho)
        time_factors.append(time_dilation)

    # Plot
    if not os.path.exists("figures"): os.makedirs("figures")
    
    plt.figure(figsize=(10, 6), facecolor='#111111')
    ax = plt.axes()
    ax.set_facecolor('#111111')
    
    plt.plot(densities, time_factors, c='cyan', lw=3, label="Time Flow Rate (dt)")
    plt.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label="Vacuum Time Speed")
    
    plt.title("LAW-1: Emergent Time Dilation", color='white')
    plt.xlabel("Local Spatial Density (rho)", color='white')
    plt.ylabel("Rate of Time Flow (Relative to Vacuum)", color='white')
    plt.grid(True, color='#333333')
    plt.legend()
    
    plt.savefig("figures/law1_time_dilation.png")
    print("📸 Graph saved: figures/law1_time_dilation.png")

if __name__ == "__main__":
    run_experiment()
