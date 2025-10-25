import os
from utils import load_audio, spectral_subtraction, save_audio, plot_waveforms, apply_noise_gate

if __name__ == "__main__":
	# Base directory
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

	# Input and output paths
	INPUT_FILE = os.path.join(BASE_DIR, "input", "noisy_audio.wav")
	OUTPUT_FILE = os.path.join(BASE_DIR, "output", "cleaned_audio.wav")

	# Load, process, and save
	y, sr = load_audio(INPUT_FILE)
	y_clean = spectral_subtraction(y, alpha=5, beta=0.0001)
	y_clean = apply_noise_gate(y_clean, threshold=0.01)
	save_audio(y_clean, OUTPUT_FILE, sr)

	print(f"Noise cancellation complete! Check the 'output/' and 'report/' folders.")

	# Plotting results
	plot_waveforms(y, y_clean)
