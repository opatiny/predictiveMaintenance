import os
import numpy as np
import matplotlib.pyplot as plt

def create_plot_folder(file_path):
    """
    Creates a subfolder "plots/<filename_without_extension>" at the project root.

    Args:
        file_path (str): Path to the .parquet file.

    Returns:
        str: Full path to the created folder.
    """
    file_name = os.path.basename(file_path)
    folder_name = file_name.replace(".parquet", "")

    # Go up to project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
    plots_root = os.path.join(project_root, "plots")
    full_folder_path = os.path.join(plots_root, folder_name)

    os.makedirs(full_folder_path, exist_ok=True)
    return full_folder_path

def save_plot(fig, folder_path, plot_name, close_fig=False):
    """
    Saves a Matplotlib figure to the specified folder as a PNG file.

    Args:
        fig (matplotlib.figure.Figure): The figure to save.
        folder_path (str): Folder where to save the plot.
        plot_name (str): Name of the plot (without extension).
        close_fig (bool): Whether to close the figure after saving.
    """
    plot_path = os.path.join(folder_path, f"{plot_name}.png")
    fig.savefig(plot_path, bbox_inches='tight')
    if close_fig:
        plt.close(fig)  # Ferme seulement si demandé

def plot_signal_with_segments(data, segments, signal_column, folder_path, show=True):
    """
    Plots the full signal with overlaid vertical lines and shaded areas for each detected segment.

    Args:
        data (pandas.DataFrame): Data containing the signal and time.
        segments (list of tuples): List of (start_time, end_time) segments.
        signal_column (str): Name of the column containing the signal.
        folder_path (str): Where to save the plot.
        show (bool): Whether to display the plot interactively.
    """
    time_col = 'timeSeconds_nogap' if 'timeSeconds_nogap' in data.columns else 'timeSeconds'

    # === Downsample if too many points ===
    max_points = 5000
    if len(data) > max_points:
        data = data.iloc[::len(data) // max_points]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data[time_col], data[signal_column], label='Signal', lw=0.5)

    for i, (start, end) in enumerate(segments):
        ax.axvline(x=start, color='red', linestyle='--', label='Start' if i == 0 else None)
        ax.axvline(x=end, color='green', linestyle='--', label='End' if i == 0 else None)
        ax.axvspan(start, end, color='orange', alpha=0.2)  # Optionnel, peut ralentir le rendu

    ax.set_xlabel("Time [s]")
    ax.set_ylabel(signal_column)
    ax.set_title("Signal with Detected Stable Segments")
    ax.grid(True)
    ax.legend(loc='upper right')  # Plus rapide que loc="best"

    # Sauvegarde
    save_plot(fig, folder_path, "signal_with_segments")

    if show:
        print("📊 Affichage du graphique (ferme la fenêtre pour continuer)...")
        plt.show(block=True)
    else:
        plt.close(fig)  # Ferme si on ne veut pas l'afficher


def plot_segment_fft(seg, time_col, filtered_signal, frequencies, amplitudes,
                     top_freqs, top_amps, segment_index, file_name, folder_path, show=True):
    """
    Plot time-domain signal and FFT with only selected frequency peaks.

    Parameters:
    - seg (pd.DataFrame): Segment of the original signal.
    - time_col (str): Name of the time column.
    - filtered_signal (np.ndarray): High-pass filtered signal.
    - frequencies (np.ndarray): Full FFT frequency array.
    - amplitudes (np.ndarray): Full FFT amplitude array.
    - top_freqs (list): Selected frequencies (retained for Excel output).
    - top_amps (list): Corresponding amplitudes of selected frequencies.
    - segment_index (int): Index of the current segment.
    - file_name (str): Name of the source data file.
    - folder_path (str): Folder where the plots should be saved.
    - show (bool): Whether to display the plot interactively.
    """
    fig, axs = plt.subplots(2, 1, figsize=(12, 6), constrained_layout=True)

    # Time domain
    axs[0].plot(seg[time_col], filtered_signal, color='steelblue')
    axs[0].set_title(f'Segment {segment_index} - Filtered Signal (>10 Hz)', fontsize=12)
    axs[0].set_xlabel('Time [s]')
    axs[0].set_ylabel('Current [A]')
    axs[0].grid(True)

    # Frequency domain
    axs[1].plot(frequencies, amplitudes, color='gray', label='Full Spectrum')
    axs[1].stem(top_freqs, top_amps, linefmt='r-', markerfmt='ro', basefmt=' ', label='Selected Peaks')
    axs[1].set_title(f'Segment {segment_index} - Frequency Peaks', fontsize=12)
    axs[1].set_xlabel('Frequency [Hz]')
    axs[1].set_ylabel('Amplitude [A]')
    axs[1].legend(loc='upper right')
    axs[1].grid(True)

    # Save
    plot_path = os.path.join(folder_path, f'fft_segment{segment_index}.png')
    fig.savefig(plot_path)

    if show:
        print(f"📊 Affichage FFT Segment {segment_index} (ferme la fenêtre pour continuer)...")
        plt.show(block=True)
    else:
        plt.close(fig)