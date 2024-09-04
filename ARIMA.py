import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt

# Load the synthetic ECG data
data = pd.read_csv('ecg_with_anomalies.csv')
data['Time'] = pd.to_datetime(data['Time'], unit='s')  # Convert time to datetime format
data.set_index('Time', inplace=True)


def detect_anomalies(ecg_data, window_size, threshold):
    # Compute moving average
    ecg_smoothed = ecg_data.rolling(window=window_size).mean()

    # Compute the difference between actual and smoothed values
    anomaly_score = np.abs(ecg_data - ecg_smoothed)

    # Detect anomalies based on the threshold
    anomalies = anomaly_score > threshold

    return anomalies

window_size = 10000  # Window size for the moving average
threshold = 0.5  # Threshold for anomaly detection


# Start measuring time
start_time = time.time()
# Apply anomaly detection
anomalies = detect_anomalies(data['Amplitude'], window_size, threshold)
# End measuring time
end_time = time.time()

# Calculate the time taken
execution_time = end_time - start_time
#execution_time=execution_time*1,000,000,000
print(f"Time to detect anomalies: {execution_time:.4f} seconds")


# Plot the ECG data with detected anomalies
'''plt.figure(figsize=(12, 4))
plt.plot(data.index, data['Amplitude'], label='ECG Data')
plt.plot(data.index, data['Amplitude'].where(anomalies), 'ro', label='Anomalies')
plt.title('ECG Data with Detected Anomalies')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.show()'''
