import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils.getFormattedSignalData import getFormattedSignalData
from fft_utils import compute_fft_features
from pca_utils import apply_pca
from plot_utils import plot_signal

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
    Process a single signal file, compute FFT, extract features, apply PCA, and plot the results.

    Parameters:
    file_path (str): The path to the CSV file containing the signal data.
    output_dir (str): The base directory where the plots will be saved.
    dataset_name (str): The name of the dataset to process.
    top_k (int): The number of top frequencies to consider for feature extraction.
    n_components (int): The number of principal components to keep for PCA.

    Returns:
    None
    """
    # Check if the file belongs to the specified dataset and signal list
    if dataset_name not in file_path or not any(signal in file_path for signal in signals_to_process):
        return

    # Load and format signal data
    data = getFormattedSignalData(file_path)

    # Ensure signal is a numpy array
    signal = np.array(data["value"].values)

    # Compute the FFT
    timestep = (data["timeSeconds"].iloc[1] - data["timeSeconds"].iloc[0]).mean()
    fft_features = compute_fft_features(signal, timestep, top_k=top_k)

    # Apply PCA to the feature vector
    reduced_features = apply_pca(fft_features.reshape(1, -1), n_components=min(n_components, len(fft_features)))

    # Plot PCA results
    pca_output_dir = os.path.join(output_dir, 'pca')
    os.makedirs(pca_output_dir, exist_ok=True)
    plt.figure()
    plt.scatter(reduced_features[:, 0], reduced_features[:, 1] if reduced_features.shape[1] > 1 else np.zeros_like(reduced_features[:, 0]))
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.title(f"PCA of {os.path.basename(file_path)}")
    plt.grid(True)
    plt.savefig(os.path.join(pca_output_dir, f"{os.path.basename(file_path)}_pca.png"))
    plt.close()
