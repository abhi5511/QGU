import numpy as np
import matplotlib.pyplot as plt
import os

def run_lennard_jones_proof():
    print("⚗️ INITIALIZING QGU CHEMISTRY PROOF...")
    print("   Testing Law-4: Can Flow-Merge create Atomic Bonding?")

    # ==========================================
    # 1. SETUP THE "FLOW FIELD" (1D Universe)
    # ==========================================
    # Space from -5 to 10 (arbitrary units)
    x = np.linspace(-5, 10, 1000)
    dx = x[1] - x[0]

    # Atom Parameters (Gaussian "Bhawar")
    sigma = 0.8  # Size of the atom
    strength = 1.0 # Intensity of flow

    def get_atom_density(center_pos):
        return strength * np.exp(-((x - center_pos)**2) / (2 * sigma**2))

    # ==========================================
    # 2. CALCULATE INTERACTION ENERGY
    # ==========================================
    # We move Atom B closer to Atom A (fixed at 0)
    distances = np.linspace(0.1, 4.0, 100)
    potential_energy = []

    # Constants for QGU Physics
    # Alpha: Gradient Energy (Attraction - Smoothing)
    # Beta: Density Compression (Repulsion - Overcrowding)
    alpha = 1.0 
    beta = 0.3  

    # Reference Energy (Single Atom)
    rho_single = get_atom_density(0)
    grad_single = np.gradient(rho_single, dx)
    E_single = np.sum(0.5 * alpha * grad_single**2 + beta * rho_single**4)
    
    # E_infinity (Two separated atoms)
    E_ref = 2 * E_single

    print("   Simulating atomic approach...")
    
    for r in distances:
        # Create Fields
        rho_A = get_atom_density(0)
        rho_B = get_atom_density(r)
        
        # Merged Field (Linear Superposition)
        rho_total = rho_A + rho_B
        
        # --- APPLY LAW-4 (Gradient Energy) ---
        # "Nature loves smooth gradients"
        grad_total = np.gradient(rho_total, dx)
        E_gradient = np.sum(0.5 * alpha * grad_total**2)
        
        # --- APPLY DENSITY COST (Repulsion) ---
        # "Space resists infinite density"
        E_compression = np.sum(beta * rho_total**4)
        
        # Interaction Energy = System - Isolated Atoms
        interaction_E = (E_gradient + E_compression) - E_ref
        potential_energy.append(interaction_E)

    # ==========================================
    # 3. VISUALIZATION
    # ==========================================
    plt.figure(figsize=(10, 6), facecolor='#111111')
    ax = plt.gca()
    ax.set_facecolor='#111111')

    # Plot the curve
    plt.plot(distances, potential_energy, color='cyan', linewidth=3, label="QGU Interaction Energy")
    
    # Mark the Bond Length (Minimum Energy)
    min_E = min(potential_energy)
    min_r = distances[potential_energy.index(min_E)]
    
    plt.scatter([min_r], [min_E], color='magenta', s=100, zorder=5, label=f"Stable Bond (r={min_r:.2f})")
    plt.axhline(0, color='gray', linestyle='--', alpha=0.5)
    
    # Annotations
    plt.text(0.5, max(potential_energy)*0.8, "REPULSION ZONE\n(Density Compression)", color='#ff5555', ha='center')
    plt.text(3.0, min_E*0.5, "ATTRACTION ZONE\n(Gradient Smoothing)", color='#55ff55', ha='center')
    plt.text(min_r, min_E - 5, "BOND FORMED", color='magenta', ha='center', fontweight='bold', va='top')

    plt.title("QGU PROOF: EMERGENT CHEMICAL BONDING", color='white', fontsize=14)
    plt.xlabel("Distance between Atoms", color='white')
    plt.ylabel("Interaction Energy", color='white')
    plt.grid(True, color='#333333', alpha=0.3)
    plt.legend()
    plt.tick_params(colors='white')

    # Save
    if not os.path.exists("figures"): os.makedirs("figures")
    save_path = "figures/qgu_chemical_bond.png"
    plt.savefig(save_path, facecolor='#111111')
    print(f"📸 Proof Generated: {save_path}")
    plt.show()

if __name__ == "__main__":
    run_lennard_jones_proof()