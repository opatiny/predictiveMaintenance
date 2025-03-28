import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.getFormattedSignalData import getFormattedSignalData
from utils.fft import compute_fft_features
from utils.plot import plot_signal

# List of signals to compute FFT for
signals_to_process = [
    "lrSigSpindleTemp", "stSigAxCurrentB", "stSigAxCurrentS", "stSigAxCurrentX",
    "stSigAxCurrentY", "stSigAxCurrentZ", "stSigAxFollErrB", "stSigAxFollErrX",
    "stSigAxFollErrY", "stSigAxFollErrZ", "stSigAxPosACSB", "stSigAxPosACSC",
    "stSigAxPosACSX", "stSigAxPosACSY", "stSigAxPosACSZ", "stSigAxPosMCSB",
    "stSigAxPosMCSC", "stSigAxPosMCSX", "stSigAxPosMCSY", "stSigAxPosMCSZ",
    "stSigAxVeloACSC", "stSigAxVeloMCSC", "stSigOperation", "stSigPowerMotS",
    "stSigSpindleIndicator", "stSigSpindleVelocity"
]

def process_signal_file(file_path, output_dir, dataset_name, top_k=10, n_components=1):
    """
    Process a single signal file, compute FFT, extract features, and plot the results.
    """
    if dataset_name not in file_path or not any(signal in file_path for signal in signals_to_process):
        return

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Load and format signal data
    data = getFormattedSignalData(file_path)

    # Ensure signal is a numpy array
    signal = np.array(data["value"].values)

    # Compute the FFT
    timestep = (data["timeSeconds"].iloc[1] - data["timeSeconds"].iloc[0]).mean()
    fft_features = compute_fft_features(signal, timestep, top_k=top_k)

    # Add frequency components to a DataFrame for plotting
    fft_data = pd.DataFrame({
        "frequency": fft_features["frequencies"],
        "magnitude": fft_features["magnitudes"]
    })

    # Get file name without extension
    file_name = os.path.basename(file_path).split(".")[0]

    # Plot and save results
    plot_signal(data, file_name, output_dir, plot_type='temporal')   # Time-domain plot
    plot_signal(fft_data, file_name, output_dir, plot_type='frequency')  # Frequency-domain plot
