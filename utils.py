import numpy as np
from scipy import signal


def generate_pulse(t, freq, n_cycles):
    """
    Generate a sinusoidal pulse with specified frequency and number of cycles.

    Args:
        t (np.array): Time vector
        freq (float): Frequency in Hz
        n_cycles (int): Number of cycles in the pulse

    Returns:
        np.array: Generated pulse signal
    """
    pulse = np.zeros_like(t)
    pulse_mask = (t >= 0) & (t <= n_cycles / freq)
    pulse[pulse_mask] = np.sin(2 * np.pi * freq * t[pulse_mask])
    return pulse


def time_shift(signal, t, phase_shift, freq):
    """
    Time shift a signal by a specified phase angle.

    Args:
        signal (np.array): Input signal to shift
        t (np.array): Time vector
        phase_shift (float): Phase shift in radians
        freq (float): Signal frequency in Hz

    Returns:
        np.array: Time-shifted signal
    """
    # Calculate time shift from phase
    time_shift = phase_shift / (2 * np.pi * freq)

    # Create shifted time vector
    t_shifted = t - time_shift

    # Interpolate signal to new time points
    shifted_signal = np.interp(t, t_shifted, signal, left=0, right=0)

    return shifted_signal


def iq_demodulate(input_signal, t, freq, fs, cutoff_freq=None):
    """
    Perform I/Q demodulation on a signal.

    Args:
        input_signal (np.array): Input signal to demodulate
        t (np.array): Time vector
        freq (float): Carrier frequency in Hz
        fs (float): Sampling frequency in Hz
        cutoff_freq (float, optional): Cutoff frequency for low-pass filter.
                                     Defaults to carrier frequency.

    Returns:
        tuple: (I component, Q component) of demodulated signal
    """
    # Perform I/Q demodulation
    demod = input_signal * np.exp(1j * 2 * np.pi * freq * t)

    # Design and apply low-pass filter
    nyquist = fs / 2
    if cutoff_freq is None:
        cutoff_freq = freq

    b, a = signal.butter(4, cutoff_freq / nyquist, btype="low")
    demod_filtered = signal.filtfilt(b, a, demod)

    # Extract I and Q components
    i_demod = np.real(demod_filtered)
    q_demod = np.imag(demod_filtered)

    return i_demod, q_demod
