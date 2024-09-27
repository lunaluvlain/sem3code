# import numpy as np
# import matplotlib.pyplot as plt

# # Data extracted from the image
# data = [-0.92, -3.71, 3.11, -0.24, 4.65, 0.84, -2.98, -3.94, -4.03, -2.51, 0.17,
#         3.85, 2.58, 0.38, 4.58, 3.4, -3.46]

# # Compute autocorrelation
# autocorrelation = np.correlate(data, data, mode='full')
# autocorrelation = autocorrelation[autocorrelation.size // 2:]  # Take the positive lags

# # Plotting autocorrelation
# plt.figure(figsize=(10, 5))
# plt.stem(range(len(autocorrelation)), autocorrelation)  # Removed the 'use_line_collection' argument
# plt.title('Autocorrelation of the Data')
# plt.xlabel('Lag')
# plt.ylabel('Autocorrelation')
# plt.grid(True)
# plt.show()

# # Find periodicity by detecting significant peaks in autocorrelation
# # Peaks that are significantly higher than the others indicate periodic behavior
# peaks = np.where(autocorrelation > 0.5 * max(autocorrelation))[0]

# # Identify periodicity if peaks are regularly spaced
# periodicity = np.diff(peaks) if len(peaks) > 1 else None

# print("Autocorrelation:", autocorrelation)
# print("Peaks:", peaks)
# print("Periodicity:", periodicity)
import numpy as np

# Define the sequences
x = np.array([8, 8, 8, 1])  # Corresponds to x[n] = 8δ[n] + 8δ[n-1] + 8δ[n-2] + δ[n-3]
h = np.array([0.5, 1, 0.5])  # Corresponds to h[n] = 0.5δ[n] + δ[n-1] + 0.5δ[n-2]

# Perform the convolution
y = np.convolve(x, h)

# Print the result
print("Convolution result y[n]:", y)