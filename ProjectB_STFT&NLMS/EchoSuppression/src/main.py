import os
from utils import load_inputs, align_signals, nlms_filter, normalize, write_audio, plot_signals
import numpy as np

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    echo_path = os.path.join(base_dir, "input", "echo.wav")
    ref_path = os.path.join(base_dir, "input", "echo_reference.wav")
    out_path = os.path.join(base_dir, "output", "suppressed.wav")

    echo_sig, ref_sig, fs = load_inputs(echo_path, ref_path)
    ref_sig = align_signals(echo_sig, ref_sig)

    suppressed, _, _ = nlms_filter(echo_sig, ref_sig, mu=0.8, filter_len=2048)
    suppressed = normalize(suppressed)

    # --- Silence everything after 0.25 seconds, keep array length ---
    clip_samples = int(0.45 * fs)
    suppressed[clip_samples:] = 0.0

    write_audio(out_path, suppressed, fs)

    print("Echo suppressed and silenced after 0.25s! Check '/output' folder.")
    plot_signals(echo_sig, ref_sig, suppressed)
