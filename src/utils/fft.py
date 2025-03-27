import numpy as np
from scipy.fft import fft

def compute_fft(signal, timestep):
    """
    Compute the FFT of a given signal.

    Parameters:
    signal (array-like): The signal data.
    timestep (float): The time step between samples.

    Returns:
    fft_values (array-like): The FFT values.
    fft_freq (array-like): The corresponding frequencies.
    """
    n = len(signal)
    fft_values = fft(signal)
    fft_freq = np.fft.fftfreq(n, d=timestep)
    return fft_values, fft_freq

def compute_fft_features(signal, timestep, top_k=10):
    """
    Compute the FFT and extract the top K frequencies with the highest amplitudes.

    Parameters:
    signal (array-like): The signal data.
    timestep (float): The time step between samples.
    top_k (int): The number of top frequencies to consider.

    Returns:
    features (array-like): The feature vector of top K frequencies.
    """
    # Compute FFT
    fft_values, fft_freq = compute_fft(signal, timestep)

    # Get the magnitudes of the FFT values
    magnitudes = np.abs(fft_values[:len(fft_values)//2])

    # Find the indices of the top K frequencies
    top_k_indices = np.argsort(magnitudes)[-top_k:]

    # Create the feature vector
    features = magnitudes[top_k_indices]

    return features
