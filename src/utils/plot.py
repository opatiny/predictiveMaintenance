import matplotlib.pyplot as plt
import os

def plot_signal(data, file_name, output_dir, plot_type):
    """
    Plot the signal data.

    Parameters:
    data (pd.DataFrame): The data to plot.
    file_name (str): The name of the file being processed.
    output_dir (str): The directory where the plot will be saved.
    plot_type (str): The type of plot ('temporal' or 'frequency').

    Returns:
    None
    """
    plt.figure()
    if plot_type == 'temporal':
        plt.plot(data["timeSeconds"], data["value"], label='Signal')
        plt.title(f"Temporal Plot of {file_name}")
        plt.xlabel("Time [s]")
    elif plot_type == 'frequency':
        plt.plot(data["frequency"], data["magnitude"], label='FFT Magnitude')
        plt.title(f"FFT of {file_name}")
        plt.xlabel("Frequency [Hz]")
    else:
        raise ValueError("Invalid plot type. Use 'temporal' or 'frequency'.")

    plt.ylabel("Amplitude")
    plt.grid(True)

    # Save the plot
    output_file = os.path.join(output_dir, f"{file_name}_{plot_type}.png")
    plt.savefig(output_file)
    plt.close()
