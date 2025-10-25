import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt


def read_audio(path):
    sig, fs = sf.read(path)
    return (sig[:, 0] if sig.ndim > 1 else sig), fs


def write_audio(path, sig, fs):
    sf.write(path, sig, fs)


def load_inputs(echo_path, ref_path):
    echo, fs1 = read_audio(echo_path)
    ref, fs2 = read_audio(ref_path)
    n = min(len(echo), len(ref))
    return echo[:n], ref[:n], fs1


def align_signals(echo, ref):
    corr = np.correlate(echo, ref, mode="full")
    lag = np.argmax(corr) - len(ref) + 1
    if lag > 0:
        ref = np.pad(ref, (lag, 0))[:len(echo)]
    elif lag < 0:
        ref = ref[-lag:]
        ref = np.pad(ref, (0, len(echo) - len(ref)))
    return ref


def nlms_filter(desired, reference, mu=0.8, filter_len=2048, eps=1e-8):
    n = len(reference)
    y, e, w = np.zeros(n), np.zeros(n), np.zeros(filter_len)
    for i in range(filter_len, n):
        x = reference[i-filter_len:i][::-1]
        y[i] = np.dot(w, x)
        e[i] = desired[i] - y[i]
        norm = np.dot(x, x) + eps
        w += (mu / norm) * e[i] * x
    return e, y, w


def normalize(sig):
    return sig / (np.max(np.abs(sig)) + 1e-9)


def plot_signals(echo, ref, out):
    plt.figure(figsize=(10, 5))
    titles = ["Echoed Input", "Aligned Reference", "Suppressed Output"]
    for i, s in enumerate([echo, ref, out], 1):
        plt.subplot(3, 1, i)
        plt.plot(s)
        plt.title(titles[i-1])
    plt.tight_layout()
    plt.show()
