import numpy as np
from scipy.signal import butter, filtfilt, find_peaks
from scipy.fft import fft, fftfreq
from collections import defaultdict
import logging
import os
import re

logging.basicConfig(level=logging.INFO)

def highpass_filter(signal, fs, cutoff=5.0, order=4):
    """
    Apply a Butterworth high-pass filter to the input signal.

    Parameters:
    - signal (np.ndarray): Input time-domain signal.
    - fs (float): Sampling frequency in Hz.
    - cutoff (float): Cutoff frequency in Hz (default=5.0).
    - order (int): Filter order (default=4).

    Returns:
    - np.ndarray: Filtered signal with zero-phase distortion.
    """
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    filtered_signal = filtfilt(b, a, signal)
    logging.debug(f"Highpass filter applied: cutoff={cutoff}Hz, order={order}")
    return filtered_signal


def extract_fft_peaks(data, segments, signal_column, file_path, folder_path, all_peaks, show=True,
                      max_freq=500, peak_prominence=0.05):
    """
    Perform FFT on given segments, detect dominant frequency peaks, plot FFT and accumulate results.

    Parameters:
    - data (pd.DataFrame): Data containing signal and time.
    - segments (list of tuples): List of (start_time, end_time) defining stable segments.
    - signal_column (str): Column name of the signal.
    - file_path (str): Source file path (used to detect sampling rate).
    - folder_path (str): Folder path where plots will be saved.
    - all_peaks (list): Accumulator list to append detected peaks.
    - max_freq (float): Maximum frequency to consider (default=500Hz).
    - peak_prominence (float): Minimum relative prominence for peak detection.

    Returns:
    - list: Updated all_peaks list containing tuples (file_path, segment_idx, frequency, amplitude).
    """
    from src.preprocessing import detect_sampling_rate
    from src.plot import plot_segment_fft

    fs = detect_sampling_rate(file_path)
    time_col = 'timeSeconds_nogap' if 'timeSeconds_nogap' in data.columns else 'timeSeconds'
    
    segment_peaks = []  # liste des (segment_idx, peak_freqs, peak_amps)

    for segment_index, (start, end) in enumerate(segments, 1):
        seg = data[(data[time_col] >= start) & (data[time_col] <= end)]
        if len(seg) < 2:
            logging.warning(f"Segment {segment_index} too short for FFT in file {os.path.basename(file_path)}")
            continue

        signal = seg[signal_column].values
        signal = highpass_filter(signal, fs, cutoff=10)
        signal -= np.mean(signal)  # Remove DC offset

        # Zero-padded FFT for better frequency resolution
        n_fft = 2 ** (int(np.ceil(np.log2(len(signal)))) + 2)
        fft_vals = fft(signal, n=n_fft)
        freqs = fftfreq(n_fft, d=1/fs)

        valid_idx = (freqs >= 0) & (freqs <= max_freq)
        amplitudes = np.abs(fft_vals[valid_idx])
        frequencies = freqs[valid_idx]

        # Peak detection parameters
        freq_resolution = frequencies[1] - frequencies[0]
        min_distance = int(10 / freq_resolution)  # minimum distance ~10 Hz
        peak_indices, _ = find_peaks(
            amplitudes,
            height=np.max(amplitudes) * peak_prominence,
            distance=min_distance
        )

        peak_freqs = frequencies[peak_indices]
        peak_amps = amplitudes[peak_indices]

        # Append detected peaks to global list
        for f, a in zip(peak_freqs, peak_amps):
            all_peaks.append((file_path, segment_index, f, a))

        # Plot FFT with peaks marked
        plot_segment_fft(
            seg,
            time_col=time_col,
            filtered_signal=signal,
            frequencies=frequencies,
            amplitudes=amplitudes,
            top_freqs=peak_freqs,
            top_amps=peak_amps,
            segment_index=segment_index,
            file_name=file_path,
            folder_path=folder_path,
            show=show
        )

        logging.info(f"Extracted {len(peak_freqs)} peaks from segment {segment_index} in file {os.path.basename(file_path)}")

        segment_peaks.append((segment_index, peak_freqs, peak_amps))
        
    return segment_peaks


def group_frequencies(all_peaks, max_groups=5, tolerance=5.0):
    """
    Group similar frequencies from detected peaks regardless of machine or segment.

    Parameters:
    - all_peaks (list): List of (file_path, segment_idx, freq, amp).
    - max_groups (int): Max number of frequency groups to return.
    - tolerance (float): Frequency tolerance in Hz for grouping.

    Returns:
    - list of dominant frequencies (freq, total_amplitude)
    """
    freq_counter = defaultdict(float)

    for _, _, freq, amp in all_peaks:
        # Normalize freq and amp to flat lists
        if isinstance(freq, np.ndarray):
            freqs = freq.flatten()
        else:
            freqs = freq if isinstance(freq, (list, tuple)) else [freq]

        if isinstance(amp, np.ndarray):
            amps = amp.flatten()
        else:
            amps = amp if isinstance(amp, (list, tuple)) else [amp]

        for f, a in zip(freqs, amps):
            matched = False
            for ref_freq in freq_counter:
                if abs(f - ref_freq) <= tolerance:
                    freq_counter[ref_freq] += a
                    matched = True
                    break
            if not matched:
                freq_counter[f] += a

    # Sort groups by total amplitude descending and keep top max_groups
    top_groups = sorted(freq_counter.items(), key=lambda x: -x[1])[:max_groups]

    logging.info(f"Grouped frequencies into {len(top_groups)} dominant groups")
    return top_groups


def group_frequencies_per_machine_segment(all_peaks, max_groups=5, tolerance=5.0):
    """
    Group frequencies separately by machine and segment.

    Parameters:
    - all_peaks (list): List of (file_path, segment_idx, freq, amp).
    - max_groups (int): Maximum number of groups per machine-segment.
    - tolerance (float): Frequency tolerance in Hz for grouping.

    Returns:
    - dict: {(machine, segment_idx): list of dominant frequencies}
    """
    machine_segment_freqs = defaultdict(list)
    grouped_results = {}

    def extract_machine(file_path):
        base = os.path.basename(file_path)
        name = base.split('.')[0]
        machine = re.match(r'^[a-zA-Z]+', name)
        return machine.group(0) if machine else name

    # Collect frequencies per machine and segment
    for file_path, segment_idx, freq, amp in all_peaks:
        # Normalize freq and amp to flat lists
        if isinstance(freq, np.ndarray):
            freqs = freq.flatten()
        else:
            freqs = freq if isinstance(freq, (list, tuple)) else [freq]

        if isinstance(amp, np.ndarray):
            amps = amp.flatten()
        else:
            amps = amp if isinstance(amp, (list, tuple)) else [amp]

        machine = extract_machine(file_path)

        for f, a in zip(freqs, amps):
            machine_segment_freqs[(machine, segment_idx)].append((f, a))

    # Group frequencies per (machine, segment)
    for key, freq_amp_list in machine_segment_freqs.items():
        freq_counter = defaultdict(float)
        for freq, amp in freq_amp_list:
            matched = False
            for ref_freq in freq_counter:
                if abs(freq - ref_freq) <= tolerance:
                    freq_counter[ref_freq] += amp
                    matched = True
                    break
            if not matched:
                freq_counter[freq] += amp

        # Sort and keep top max_groups frequencies
        top_groups = sorted(freq_counter.items(), key=lambda x: -x[1])[:max_groups]
        grouped_results[key] = [freq for freq, _ in top_groups]

    logging.info(f"Grouped frequencies per machine and segment with {len(grouped_results)} groups")
    return grouped_results