import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import cwt, ricker

# Generate a sample signal
t = np.linspace(0, 1, num=1000)
with open(r"C:\Users\ubicomplab\Downloads\sdrdataread\test1.txt", 'r') as file:
    signal = file.readlines() 

# Define parameters
widths = np.arange(1, len(signal))  # Range of scales
wavelet = ricker

# Perform CWT using Ricker wavelet
cwt_matrix = cwt(signal, wavelet, widths)

# Plot the CWT results
plt.figure(figsize=(10, 6))
plt.imshow(np.abs(cwt_matrix), extent=[0, 1, 1, 100], cmap='coolwarm', aspect='auto')
plt.colorbar(label='Magnitude')
plt.title('Continuous Wavelet Transform using Ricker (Mexican Hat) Wavelet')
plt.xlabel('Time')
plt.ylabel('Scale')
plt.show()
