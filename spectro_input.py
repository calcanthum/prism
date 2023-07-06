import pandas as pd
import os

def load_csv_data(filepath):
    """
    This function loads the CSV data from the provided file path.

    Parameters:
    filepath (str): The file path of the data CSV.

    Returns:
    pd.DataFrame: The loaded dataframe.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"File {filepath} does not exist.")
    try:
        return pd.read_csv(filepath)
    except Exception as e:
        raise Exception(f"Failed to load csv data from {filepath} due to: {str(e)}")

def reshape_spectro_data(spectro_data):
    """
    This function reshapes the spectroscopic data into long format.

    Parameters:
    spectro_data (pd.DataFrame): The spectroscopic data.

    Returns:
    pd.DataFrame: The reshaped dataframe.
    """
    if 'sample_id' not in spectro_data.columns:
        raise ValueError("'sample_id' is not present in spectro_data DataFrame.")
    try:
        return spectro_data.melt(id_vars='sample_id', var_name='wavelength', value_name='absorbance')
    except Exception as e:
        raise Exception("Failed to reshape spectro data due to: ", str(e))

def merge_data(spectro_data, concentration_data):
    """
    This function merges the spectroscopic data and concentration data.

    Parameters:
    spectro_data (pd.DataFrame): The reshaped spectroscopic data.
    concentration_data (pd.DataFrame): The concentration data.

    Returns:
    pd.DataFrame: The merged dataframe.
    """
    if 'sample_id' not in spectro_data.columns or 'sample_id' not in concentration_data.columns:
        raise ValueError("'sample_id' is not present in one or both of the dataframes.")
    try:
        return pd.merge(spectro_data, concentration_data, on='sample_id')
    except Exception as e:
        raise Exception("Failed to merge data due to: ", str(e))