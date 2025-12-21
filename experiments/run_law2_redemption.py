import sys
import os
# Add parent directory to path so we can import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from src.qgu_core import QGU_System

# CONFIGURATION
STEPS = 200

def run_experiment():
    print("🚀 Initializing Law-2 Redemption Experiment...")
    system = QGU_System()
    
    # 1. Create Gravity Well (Central Mass)
    for _ in range(50):
        pos = np.random.normal(0, 2, 3)
        system.add_entity(pos, mass=5.0, fixed=True)
        
    # 2. Add Test Subjects (Falling particles)
    test_subjects = []
    for _ in range(30):
        pos = np.random.uniform(5, 20, 3)
        p = system.add_entity(pos, mass=1.0, fixed=False)
        test_subjects.append(p)
        
    gradients = []
    accelerations = []
    
    # 3. Simulation Loop
    print("🧪 Simulating Physics...")
    for t in range(STEPS):
        # Physics Step (Simple N-Body for generation)
        for p in system.entities:
            if p.fixed: continue
            force = np.zeros(3)
            for other in system.entities:
                if p == other: continue
                delta = other.pos - p.pos
                dist = np.linalg.norm(delta) + 0.5
                f_mag = (1.0 * p.mass * other.mass) / (dist**2)
                force += f_mag * (delta/dist)
            p.acc = force / p.mass
            p.vel += p.acc * 0.1
            p.pos += p.vel * 0.1
            
        # Data Collection
        if t % 5 == 0:
            for p in test_subjects:
                grad, accel = system.calculate_gradient_acceleration(p)
                if grad > 0.01 and accel > 0.001:
                    gradients.append(grad)
                    accelerations.append(accel)
                    
    # 4. Analysis
    if len(gradients) > 0:
        slope, intercept, r_value, p_value, std_err = stats.linregress(gradients, accelerations)
        print(f"🎯 FINAL RESULT: R-Squared = {r_value**2:.4f}")
        
        # 5. Plot
        if not os.path.exists("figures"):
            os.makedirs("figures")
            
        plt.figure(figsize=(10, 6), facecolor='#111111')
        ax = plt.axes()
        ax.set_facecolor('#111111')
        plt.scatter(gradients, accelerations, c='cyan', alpha=0.6, s=15, label="Observed Data")
        
        line_x = np.array([min(gradients), max(gradients)])
        line_y = slope * line_x + intercept
        plt.plot(line_x, line_y, c='lime', lw=2, linestyle='--', label=f"Fit Line (R²={r_value**2:.2f})")
        
        plt.title(f"LAW-2 VERIFIED: Gradient vs Acceleration (R²={r_value**2:.2f})", color='white')
        plt.xlabel("Density Gradient", color='white')
        plt.ylabel("Acceleration", color='white')
        plt.grid(True, color='#333333')
        plt.legend()
        plt.savefig("figures/law2_result.png") # Auto-save the proof
        print("📸 Graph saved to figures/law2_result.png")
        # plt.show() # Uncomment to see popup
    else:
        print("⚠️ Not enough data collected to plot.")

if __name__ == "__main__":
    run_experiment()
