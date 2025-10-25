import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import librosa


def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=None)
    return y, sr


def save_audio(y, output_path, sr):
    sf.write(output_path, y, sr)


def spectral_subtraction(y, n_fft=1024, hop_length=512, alpha=2.5, beta=0.01):
    Y = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    magnitude, phase = np.abs(Y), np.angle(Y)

    # Estimate noise from low-energy frames
    frame_energy = np.mean(magnitude, axis=0)
    threshold = np.percentile(frame_energy, 30)
    noise_frames = magnitude[:, frame_energy < threshold]
    noise_est = np.mean(noise_frames, axis=1, keepdims=True)

    # Spectral subtraction
    magnitude_clean = np.maximum(
        magnitude - alpha * noise_est, beta * noise_est)
    Y_clean = magnitude_clean * np.exp(1j * phase)
    y_clean = librosa.istft(Y_clean, hop_length=hop_length)
    return y_clean


def apply_noise_gate(y_clean, threshold=0.005):
    y_clean[np.abs(y_clean) < threshold] = 0
    return y_clean


def plot_waveforms(primary, clean_speech=None):
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(primary)
    plt.title("Noisy Audio")
    if clean_speech is not None:
        plt.subplot(2, 1, 2)
        plt.plot(clean_speech[:len(primary)])
        plt.title("Cleaned Audio")
    plt.tight_layout()
    plt.show()
