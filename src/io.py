import os
import polars as pl
import numpy as np
import pandas as pd
from collections import defaultdict


def load_parquet_file(path):
    """
    Load a .parquet file using Polars for fast and efficient data loading.

    Parameters:
    - path (str): Path to the .parquet file.

    Returns:
    - pl.DataFrame: Polars DataFrame loaded from the file.
    """
    return pl.read_parquet(path)


class FrequencyClusterer:
    def __init__(self, tolerance=0.5):
        self.tolerance = tolerance
        self.raw_peaks = []  # [(file, segment, freq, amp)]

    def add_peaks(self, file_name, segment_idx, freqs, amps):
        base_file = os.path.basename(file_name)
        for f, a in zip(freqs, amps):
            self.raw_peaks.append((base_file, segment_idx, f, a))

    def _cluster_frequencies(self):
        # Group all frequencies regardless of segment to find global groups
        all_freqs = np.array([f for _, _, f, _ in self.raw_peaks])
        used = np.zeros(len(all_freqs), dtype=bool)

        clusters = []
        for i, f in enumerate(all_freqs):
            if used[i]:
                continue
            cluster = [f]
            used[i] = True
            for j in range(i + 1, len(all_freqs)):
                if not used[j] and abs(all_freqs[j] - f) <= self.tolerance:
                    cluster.append(all_freqs[j])
                    used[j] = True
            clusters.append(cluster)

        # Compute average frequency per cluster
        grouped_freqs = [round(np.mean(c), 4) for c in clusters]
        return grouped_freqs

    def _match_to_group(self, freq, groups):
        for g in groups:
            if abs(freq - g) <= self.tolerance:
                return g
        return None

    def build_tables(self):
        freq_table = defaultdict(dict)  # group_freq -> {file: {segment_freq_key: precise freq}}
        amp_table = defaultdict(dict)   # group_freq -> {file: {segment_freq_key: amplitude}}

        # Get final frequency groups
        freq_groups = self._cluster_frequencies()

        for file, segment, freq, amp in self.raw_peaks:
            group_freq = self._match_to_group(freq, freq_groups)
            if group_freq is None:
                continue  # shouldn't happen
            label = f"segment{segment}_freq{round(group_freq, 1)}"

            if file not in freq_table[group_freq]:
                freq_table[group_freq][file] = {}
                amp_table[group_freq][file] = {}

            freq_table[group_freq][file][label] = freq
            amp_table[group_freq][file][label] = amp

        return freq_table, amp_table

    def _to_dataframe(self, table, value_type="frequency"):
        all_rows = set()
        all_files = set()
        for per_file in table.values():
            for file_name, segments in per_file.items():
                all_files.add(file_name)
                all_rows.update(segments.keys())

        all_rows = sorted(all_rows)
        all_files = sorted(all_files)

        data = []
        for row_key in all_rows:
            row = []
            for file in all_files:
                val = np.nan
                for f_master in table:
                    if row_key in table[f_master].get(file, {}):
                        val = table[f_master][file][row_key]
                        break
                row.append(val)
            data.append([row_key] + row)

        df = pd.DataFrame(data, columns=["segment_freq"] + all_files)
        return df

    def to_frequency_dataframe(self):
        freq_table, _ = self.build_tables()
        return self._to_dataframe(freq_table, "frequency")

    def to_amplitude_dataframe(self):
        _, amp_table = self.build_tables()
        return self._to_dataframe(amp_table, "amplitude")

    def save_excels(self, freq_path, amp_path):
        freq_df = self.to_frequency_dataframe()
        amp_df = self.to_amplitude_dataframe()

        os.makedirs(os.path.dirname(freq_path), exist_ok=True)
        freq_df.to_excel(freq_path, index=False)
        amp_df.to_excel(amp_path, index=False)

        print(f"✅ Frequency table saved to {freq_path}")
        print(f"✅ Amplitude table saved to {amp_path}")
