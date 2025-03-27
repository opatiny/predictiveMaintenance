import os
from signal_processing import process_signal_file

def process_signals_in_directory(input_dir, output_dir, dataset_name):
    """
    Process all signal files in a directory and save plots for the specified dataset.

    Parameters:
    input_dir (str): The directory containing the signal CSV files.
    output_dir (str): The base directory where the plots will be saved.
    dataset_name (str): The name of the dataset to process.

    Returns:
    None
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process each file in the input directory
    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        process_signal_file(file_path, output_dir, dataset_name)

if __name__ == "__main__":
    input_directory = 'data/mecatis/Warmup_Mecatis_03_02_25'
    output_directory = 'plots/mecatis/Warmup_Mecatis_03_02_25'
    dataset_name = 'Warmup_Mecatis_03_02_25'
    process_signals_in_directory(input_directory, output_directory, dataset_name)
