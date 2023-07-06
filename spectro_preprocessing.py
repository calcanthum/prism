import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
from scipy.stats import zscore
import pywavelets as pywt

# Load the data
df = pd.read_csv('your_file.csv')

# Set the sample id as index
df.set_index('sample_id', inplace=True)

# Outlier detection
z_scores = np.abs(zscore(df))
df_no_outliers = df[(z_scores < 3).all(axis=1)]  # Consider as outlier if z-score is larger than 3

# Apply Savitzky-Golay smoothing
df_smooth = savgol_filter(df_no_outliers.values, window_length=5, polyorder=3, axis=0)
df_smooth = pd.DataFrame(df_smooth, index=df_no_outliers.index, columns=df_no_outliers.columns)

# Wavelet denoising
wavelet = pywt.Wavelet('db6')
coeffs = pywt.wavedec(df_smooth.values, wavelet, level=9, axis=0)
for i in range(1, len(coeffs)):
    coeffs[i] = pywt.threshold(coeffs[i], value=0.5*np.sqrt(2*np.log(len(df_smooth.values))), mode='soft')
df_denoised = pywt.waverec(coeffs, wavelet, axis=0)
df_denoised = pd.DataFrame(df_denoised, index=df_smooth.index, columns=df_smooth.columns)

# Apply Standard Normal Variate (SNV)
df_snv = (df_denoised - np.mean(df_denoised, axis=0)) / np.std(df_denoised, axis=0)

print("Preprocessing completed")

# Save preprocessed data to a new CSV file
df_snv.to_csv('preprocessed_spectra.csv')
