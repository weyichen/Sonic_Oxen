from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz

fs = 500
nyq = 0.5 * fs
lowcut = 0.5
highcut = 50
low = lowcut / nyq
high = highcut / nyq
b, a = butter(5, [low, high], btype='band')

# Plot the frequency response for a few different orders.

plt.figure(1)
plt.clf()
w, h = freqz(b, a, worN = 2000)
plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = 5")

plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
         '--', label='sqrt(0.5)')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain')
plt.grid(True)
plt.legend(loc='best')
plt.show()
print w