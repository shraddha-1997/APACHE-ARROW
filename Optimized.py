import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import pyarrow.csv as csv
import pyarrow as pa

# Function to detect anomalies using moving average
def detect_anomalies(ecg_data, window_size, threshold):
    ecg_smoothed = ecg_data.rolling(window=window_size).mean()
    anomaly_score = np.abs(ecg_data - ecg_smoothed)
    anomalies = anomaly_score > threshold
    return anomalies

# Load synthetic ECG data from CSV file into Pandas DataFrame
df = csv.read_csv('ecg_with_anomalies.csv').to_pandas()

# Convert 'Time' column to datetime format (assuming 'Time' is in seconds)
df['Time'] = pd.to_datetime(df['Time'], unit='s')

# Set parameters for anomaly detection
window_size = 100
threshold = 0.5

# Measure the time taken for anomaly detection
start_time = time.time()
anomalies = detect_anomalies(df['Amplitude'], window_size, threshold)
end_time = time.time()
execution_time = end_time - start_time

print(f"Time to detect anomalies: {execution_time:.4f} seconds")

# Plot the ECG data with detected anomalies
# plt.figure(figsize=(12, 4))
# plt.plot(df['Time'], df['Amplitude'], label='ECG Data')
# plt.plot(df['Time'][anomalies], df['Amplitude'][anomalies], 'ro', markersize=5, label='Anomalies')
# plt.title('ECG Data with Detected Anomalies')
# plt.xlabel('Time')
# plt.ylabel('Amplitude')
# plt.legend()
# plt.grid(True)
# plt.show()
