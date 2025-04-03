import pandas as pd
import os


def saveNormalizedSamples(samples: list, names: list, output_dir: str) -> None:
    """
    Save normalized samples to a parquet files.

    Args:
        samples (list): List of normalized samples.
        output_dir (str): Directory to save the parquet files.
    """

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # loop through all samples
    for i, sample in enumerate(samples):
        # Create a DataFrame from the sample
        df = pd.DataFrame(sample)

        # Save the DataFrame to a parquet file
        df.to_parquet(os.path.join(output_dir, names[i] + ".parquet"), index=False)
