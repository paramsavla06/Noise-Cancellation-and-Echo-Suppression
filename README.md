# Noise Cancellation and Echo Cancellation Project

## Overview
This project provides two audio processing pipelines to improve the quality of recorded audio:

1. **Echo Suppression using NLMS Adaptive Filtering** – removes echoes from a recorded signal using a reference echo signal and the Normalized Least Mean Squares (NLMS) algorithm.  
2. **Noise Cancellation using Spectral Subtraction** – reduces stationary background noise from audio recordings using spectral subtraction techniques, optionally with a noise gate.  

Both pipelines include visualization tools to inspect the input and output waveforms.

---

## Description

### NLMS Echo Suppression
The NLMS Echo Suppression pipeline is designed to remove unwanted echoes from a microphone signal. The pipeline takes two inputs: the microphone signal containing speech and echo, and a reference signal containing only the echo. Using an adaptive filter, the algorithm estimates the echo component and subtracts it from the microphone signal. The output is a clean, echo-suppressed audio signal, optionally silencing or clipping the audio after a specified time while keeping the overall length intact.

### Spectral Subtraction Noise Reduction
The Spectral Subtraction pipeline is used to reduce stationary background noise in audio recordings. The algorithm estimates the noise spectrum from low-energy portions of the signal and subtracts it from the spectral magnitude of the noisy signal. A noise gate can be applied afterward to remove residual low-level noise. This method does not require a separate reference signal and is effective for consistent background noise environments.

---

## How It Works

### NLMS Echo Suppression
1. **Reference Alignment** – The reference echo signal is aligned with the microphone input using cross-correlation to account for any delay.  
2. **Adaptive Filtering** – The NLMS algorithm iteratively updates filter coefficients to minimize the error between the microphone input and the estimated echo.  
3. **Output Generation** – The estimated echo is subtracted from the microphone input to produce a suppressed output. Optional clipping or silencing can be applied after a specified time.

### Spectral Subtraction Noise Reduction
1. **Short-Time Fourier Transform (STFT)** – Converts the audio signal into the frequency domain.  
2. **Noise Estimation** – Identifies low-energy frames as noise and computes an average noise spectrum.  
3. **Magnitude Subtraction** – The noise spectrum is subtracted from the original spectral magnitude with a minimum magnitude floor to avoid negative values.  
4. **Inverse STFT** – Converts the processed spectrum back to the time domain.  
5. **Optional Noise Gate** – Low-amplitude residual signals below a threshold are set to zero to further reduce noise.

Both methods include plotting functions to visualize the input and output signals for analysis and verification.
