import numpy as np
import matplotlib.pyplot as plt


def generate_normal_ecg(fs, duration):
    t = np.linspace(0, duration, int(fs*duration), endpoint=False)  # Time vector
    heart_rate = 60  # Normal heart rate in beats per minute
    ecg = np.sin(2 * np.pi * heart_rate * t)  # Basic sinusoidal ECG
    return ecg, t


def add_irregular_heartbeat(ecg, fs, duration):
    # Generate irregular heartbeat anomaly
    anomaly = np.random.normal(loc=0.2, scale=0.05, size=int(fs*duration))
    ecg_with_anomaly = ecg + anomaly
    return ecg_with_anomaly


fs = 1000  # Sampling frequency (samples per second)
duration = 1000  # Duration of ECG signal in seconds

# Generate normal ECG
ecg_normal, t = generate_normal_ecg(fs, duration)

# Introduce anomalies
ecg_with_anomaly = add_irregular_heartbeat(ecg_normal, fs, duration)

# Plot the ECG signals
plt.figure(figsize=(12, 4))
plt.plot(t, ecg_with_anomaly, label='ECG with Anomaly')
plt.plot(t, ecg_normal, 'r', alpha=0.5, label='Normal ECG')
plt.title('ECG with Anomalies')
plt.xlabel('Time (seconds)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.show()


# Prepare data for saving
data_to_save = np.column_stack((t, ecg_with_anomaly))

# Save to CSV file
np.savetxt('ecg_with_anomalies.csv', data_to_save, delimiter=',', header='Time,Amplitude', comments='')
