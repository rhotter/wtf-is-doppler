# %%
%load_ext autoreload
%autoreload 2

import numpy as np
import matplotlib.pyplot as plt
import utils

# %%
# Create time vector for 2 MHz signal
fs = 40e6  # Sampling frequency (10x signal frequency for good resolution)
n_cycles = 5
t = np.arange(-4e-6, 4e-6, 1 / fs)  # Time vector with padding

# Generate single pulse
freq = 2e6  # 2 MHz frequency
pulse = utils.generate_pulse(t, freq, n_cycles)

# Plot the pulse
plt.figure(figsize=(10, 4))
plt.plot(t * 1e6, pulse)
plt.grid(True)
plt.xlabel("Time (μs)")
plt.ylabel("Amplitude")
plt.title("2 MHz Pulse")
plt.show()

# %%
# Perform I/Q demodulation
i_demod, q_demod = utils.iq_demodulate(pulse, t, freq, fs)

# Plot I/Q components
plt.figure()
plt.plot(t * 1e6, i_demod, label="I Component")
plt.plot(t * 1e6, q_demod, label="Q Component")
plt.grid(True)
plt.xlabel("Time (μs)")
plt.ylabel("Amplitude")
plt.title("I/Q Components")
plt.legend()
plt.show()

# %%
