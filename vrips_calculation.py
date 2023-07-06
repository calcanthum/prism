from ripser import ripser
from scipy.spatial.distance import pdist, squareform
import pandas as pd
import numpy as np

def calculate_distance_matrix(group):
    """
    This function calculates the distance matrix for a group of data points.

    Parameters:
    group (pd.DataFrame): The group of data points.

    Returns:
    np.array: The distance matrix.
    """
    if 'wavelength' not in group.columns or 'absorbance' not in group.columns:
        raise ValueError("'wavelength' or 'absorbance' is not present in group DataFrame.")
    try:
        print(f"Calculating distance matrix for sample_id: {group['sample_id'].iloc[0]}")
        points = group[['wavelength', 'absorbance']].values
        return squareform(pdist(points))
    except Exception as e:
        raise Exception("Failed to calculate distance matrix due to: ", str(e))

def calculate_vietoris_rips_complex(dist_matrix, sample_id):
    """
    This function calculates the Vietoris-Rips complex for a distance matrix.

    Parameters:
    dist_matrix (np.array): The distance matrix.

    Returns:
    list: The Vietoris-Rips complex.
    """
    try:
        print(f"Calculating Vietoris-Rips complex for sample_id: {sample_id}")
        return ripser(dist_matrix, maxdim=2, distance_matrix=True)['dgms']
    except Exception as e:
        raise Exception("Failed to calculate Vietoris-Rips complex due to: ", str(e))

def calculate_all_vietoris_rips_complexes(df):
    """
    This function calculates the Vietoris-Rips complexes for all groups in the dataframe.

    Parameters:
    df (pd.DataFrame): The dataframe.

    Returns:
    dict: A dictionary of Vietoris-Rips complexes.
    """
    # Convert 'wavelength' and 'absorbance' columns to numeric types
    df['wavelength'] = pd.to_numeric(df['wavelength'], errors='coerce')
    df['absorbance'] = pd.to_numeric(df['absorbance'], errors='coerce')

    if 'sample_id' not in df.columns:
        raise ValueError("'sample_id' is not present in df DataFrame.")
    try:
        complexes = {}
        groups = df.groupby('sample_id')
        total_samples = len(groups)
        print(f"Total samples to process: {total_samples}")
        for i, (name, group) in enumerate(groups, start=1):
            print(f"\nProcessing sample {i} of {total_samples} (sample_id: {name})")
            dist_matrix = calculate_distance_matrix(group)
            complexes[name] = calculate_vietoris_rips_complex(dist_matrix, name)
        print(f"All {total_samples} samples processed.")
        return complexes
    except Exception as e:
        raise Exception("Failed to calculate all Vietoris-Rips complexes due to: ", str(e))
