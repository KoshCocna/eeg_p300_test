import numpy as np
import pandas as pd
from PIL import Image
import random
import matplotlib.pyplot as plt
import os
from pathlib import Path

# ==========================================================
# Create results folder if not exists
# ==========================================================
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)


# ==========================================================
# 1) ODDBALL STIMULUS GENERATION
# ==========================================================

def generate_oddball_stimulus():
    print("\n[1] Generating oddball stimulus...")

    DURATION = 10     # seconds
    FPS = 1           # 1Hz
    TOTAL_FRAMES = DURATION * FPS
    ODDBALL_RATIO = 0.6
    IMG_SIZE = (300, 300)

    OUT_GIF = os.path.join(RESULTS_DIR, "oddball.gif")
    OUT_CSV = os.path.join(RESULTS_DIR, "oddball_input.csv")

    frame_duration = 1.0 / FPS
    n_oddball = int(round(TOTAL_FRAMES * ODDBALL_RATIO))

    oddball_indices = set(random.sample(range(TOTAL_FRAMES), n_oddball))

    frames = []
    records = []

    for i in range(TOTAL_FRAMES):
        t = i * frame_duration

        if i in oddball_indices:
            color = (255, 0, 0)  # red (Oddball)
            label = 1
        else:
            color = (255, 255, 255)  # white (Normal)
            label = 0

        img = Image.new("RGB", IMG_SIZE, color)
        frames.append(img)

        records.append({
            "frame": i,
            "time_sec": float(t),
            "is_oddball": label
        })

    # Save GIF
    frames[0].save(
        OUT_GIF,
        save_all=True,
        append_images=frames[1:],
        duration=int(frame_duration * 1000),
        loop=0
    )

    # Save CSV
    df = pd.DataFrame(records)
    df.to_csv(OUT_CSV, index=False)

    print(f"  -> Saved: {OUT_GIF}, {OUT_CSV}")
    return OUT_CSV


# ==========================================================
# 2) FAKE EEG GENERATION BASED ON ODDBALL TIMELINE
# ==========================================================

def generate_fake_eeg(oddball_csv):
    print("\n[2] Generating fake EEG based on oddball timeline...")

    EEG_SFREQ = 250
    DURATION = 10.0
    N_SAMPLES = int(EEG_SFREQ * DURATION)
    N_CHANNELS = 24

    OUT_CSV = os.path.join(RESULTS_DIR, "epoch_p300.csv")

    oddball = pd.read_csv(oddball_csv)
    oddball_times = oddball.loc[oddball["is_oddball"] == 1, "time_sec"].values

    # Time axis
    t = np.arange(0, DURATION, 1/EEG_SFREQ)
    if t.size != N_SAMPLES:
        t = np.linspace(0, DURATION, N_SAMPLES, endpoint=False)

    # Base EEG noise
    eeg = np.random.randn(N_SAMPLES, N_CHANNELS) * 0.3

    # P300 model parameters
    P300_LAT = 0.30
    P300_WIDTH = 0.05
    AMP = 3.0

    # Channels with strongest P300 (midline)
    strong_ch = [3, 4, 17]  # Fz, Pz, Cz
    # Channels with weaker P300
    weak_ch = [0,1,2,5,6,7,16,18,23]

    # Insert P300 for each oddball
    for t0 in oddball_times:
        peak = t0 + P300_LAT
        p300 = AMP * np.exp(-0.5 * ((t - peak) / P300_WIDTH) ** 2)

        for c in strong_ch:
            eeg[:, c] += p300

        for c in weak_ch:
            eeg[:, c] += 0.5 * p300

    # Save EEG to CSV
    df = pd.DataFrame(eeg, columns=[f"ch{i}" for i in range(N_CHANNELS)])
    df.insert(0, "timestamp_sec", t)
    df.to_csv(OUT_CSV, index=False)

    print(f"  -> Saved: {OUT_CSV}")
    return OUT_CSV


# ==========================================================
# 3) P300 ERP EXTRACTION & PLOTTING
# ==========================================================

def plot_p300(eeg_csv, oddball_csv):
    print("\n[3] Extracting & plotting P300 ERP...")

    TARGET_CHANNEL = "ch3"  # Fz (P300 strongest)
    TMIN = -0.2
    TMAX = 0.8

    eeg = pd.read_csv(eeg_csv)
    times = eeg["timestamp_sec"].values
    signal = eeg[TARGET_CHANNEL].values

    oddball = pd.read_csv(oddball_csv)
    oddball_times = oddball.loc[oddball["is_oddball"] == 1, "time_sec"].values

    sfreq = 1.0 / np.median(np.diff(times))

    n_pre = int(abs(TMIN) * sfreq)
    n_post = int(TMAX * sfreq)

    epochs = []

    for t0 in oddball_times:
        idx = np.argmin(np.abs(times - t0))

        if idx - n_pre < 0 or idx + n_post >= len(signal):
            continue

        epoch = signal[idx - n_pre : idx + n_post]
        epochs.append(epoch)

    epochs = np.array(epochs)
    erp = epochs.mean(axis=0)
    t_axis = np.linspace(TMIN, TMAX, erp.size, endpoint=False)

    # Plot
    plt.figure(figsize=(10,5))

    for ep in epochs:
        plt.plot(t_axis, ep, color="gray", alpha=0.3)

    plt.plot(t_axis, erp, color="red", linewidth=2, label="Average ERP")
    plt.axvline(0, linestyle="--", color="black")
    plt.axvspan(0.25, 0.45, color="orange", alpha=0.3, label="P300 window")

    plt.title("P300 ERP (Fake EEG Based on Oddball)")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # --- P300 peak window highlight (0.2s ~ 0.4s) ---
    try:
        plt.axvspan(0.2, 0.4, alpha=0.15, label="P300 Window")
        plt.legend(loc="best")
    except Exception:
        pass

    # --- Save figure to project root folder ---
    png_path = Path("p300_peak_visualization.png")
    plt.savefig(png_path, dpi=300, bbox_inches="tight")
    print(f"P300 visualization saved to: {png_path.resolve()}")
    plt.show()
# ==========================================================
# MAIN PIPELINE
# ==========================================================

if __name__ == "__main__":
    oddball_csv = generate_oddball_stimulus()
    eeg_csv = generate_fake_eeg(oddball_csv)
    plot_p300(eeg_csv, oddball_csv)

