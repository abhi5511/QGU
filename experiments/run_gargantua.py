import os
import time
import numpy as np
import matplotlib.pyplot as plt

def run_progressive_gargantua():
    print("⚫ INITIALIZING GARGANTUA RAY-TRACER")
    print("   Mode: Progressive Scanline Rendering")
    print("   Physics: GR-inspired (Schwarzschild + Fake Kerr)")
    print("   Resolution: 1280 x 720")

    # ==========================================
    # 1. CONFIGURATION
    # ==========================================
    W, H = 1280, 720
    BH_MASS = 1.0
    RS = 2.0 * BH_MASS

    # Accretion disk
    DISK_INNER = 3.0 * RS
    DISK_OUTER = 14.0 * RS
    INCLINATION = np.deg2rad(80)

    # Fake Kerr spin (illusion only)
    SPIN = 0.3

    # Output buffer
    final_img = np.zeros((H, W, 3))

    # ==========================================
    # 2. PLOT SETUP
    # ==========================================
    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 7), facecolor="black")
    ax.set_facecolor("black")
    ax.axis("off")

    display_img = ax.imshow(
        final_img,
        extent=[-20, 20, -12, 12],
        origin="lower"
    )

    plt.title("RENDERING GARGANTUA: 0%", color="white")
    plt.tight_layout()

    # ==========================================
    # 3. PROGRESSIVE RENDER LOOP
    # ==========================================
    CHUNK_SIZE = 10
    total_chunks = H // CHUNK_SIZE
    start_time = time.time()

    for i in range(total_chunks):
        y_end = H - i * CHUNK_SIZE
        y_start = max(0, y_end - CHUNK_SIZE)

        y, x = np.ogrid[y_start:y_end, 0:W]

        # Screen → physical space mapping
        x_phys = ((x / W) - 0.5) * 40.0
        y_phys = ((y / H) - 0.5) * 24.0

        r_screen = np.sqrt(x_phys**2 + y_phys**2) + 1e-6

        # ======================================
        # PHYSICS ENGINE
        # ======================================

        # Gravitational lensing (approx)
        deflection = 4.0 * BH_MASS / r_screen

        # Fake Kerr frame dragging
        x_twist = x_phys + SPIN * np.log(r_screen + 1)

        r_disk = np.sqrt(
            x_twist**2 +
            (y_phys / np.cos(INCLINATION) + deflection)**2
        )

        # Disk mask
        disk_mask = (r_disk > DISK_INNER) & (r_disk < DISK_OUTER)

        # Doppler beaming
        velocity = 0.5 / np.sqrt(r_disk + 0.05)
        doppler = 1.0 + velocity * (x_phys / r_screen) * np.sin(INCLINATION)
        intensity = disk_mask * (doppler**4) / (r_disk + 0.3)

        # Disk thickness (vertical fade)
        thickness = np.exp(-np.abs(y_phys) * 0.15)
        intensity *= thickness

        # Temperature gradient
        temperature = np.clip(1.5 / (r_disk + 0.5), 0, 1)

        # Bloom (cinematic glow)
        bloom = np.clip(intensity - 0.6, 0, 1)

        # Color mapping (hot → blue, cool → red)
        r = intensity * (0.8 + 0.2 * temperature) + bloom * 0.6
        g = intensity * (0.4 + 0.5 * temperature) + bloom * 0.5
        b = intensity * (0.2 + 0.8 * temperature**2) + bloom * 0.4

        # Photon ring
        photon_ring = (r_screen > 2.58 * RS) & (r_screen < 2.62 * RS)
        r += photon_ring * 1.0
        g += photon_ring * 1.0
        b += photon_ring * 1.2

        # Soft event horizon shadow
        shadow = np.clip((2.8 * RS - r_screen) / (0.3 * RS), 0, 1)
        r *= (1 - shadow)
        g *= (1 - shadow)
        b *= (1 - shadow)

        # Compose chunk
        chunk_rgb = np.dstack((r, g, b))
        chunk_rgb = np.clip(chunk_rgb, 0, 1)

        final_img[y_start:y_end, :, :] = chunk_rgb

        # ======================================
        # LIVE UPDATE
        # ======================================
        display_img.set_data(final_img)
        progress = int((i + 1) / total_chunks * 100)
        plt.title(f"RENDERING GARGANTUA: {progress}%", color="white")

        if i % 2 == 0:
            plt.draw()
            plt.pause(0.001)

    print(f"✅ Render Complete in {time.time() - start_time:.2f} seconds")

    # ==========================================
    # SAVE OUTPUT
    # ==========================================
    os.makedirs("figures", exist_ok=True)
    plt.savefig(
        "figures/gargantua_final.png",
        dpi=150,
        facecolor="black"
    )
    print("📸 Saved → figures/gargantua_final.png")

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    run_progressive_gargantua()
