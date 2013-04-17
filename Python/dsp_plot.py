from scipy.signal import butter, lfilter
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz
import math

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
db = [20 * math.log10(abs(g)) for g in h]
plt.plot((fs * 0.5 / np.pi) * w[:len(w) / 3], db[:len(db) / 3], label="order = 5")

plt.plot([0, fs / 6], [-3, -3],
         '--', label='-3 db')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain')
plt.grid(True)
plt.legend(loc='best')
plt.show()
print w