import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import os
from data_reader import ReadData
from data_formatter import DataFormatter
from params import Params

# %%
params = Params()

nexdata = ReadData(params.filename, os.getcwd() + params.directory)
data = DataFormatter(nexdata.raw_data, params.well_events, params.eating_events, params.colors)
data_trials = data.trials

# %%

def fft(spike_times: np.ndarray):
    """
    Calculate the FFT of spike times
    Parameters:
    ___________
    spike_times: array
        Array of spike times
    sampling_frequency: float
        Sampling frequency of the spike times
    Returns:
    ________
    freqs: array
        Array of frequencies
    spike_fft: array
        Array of FFT output
    """
    # Calculate the time intervals between spikes
    time_intervals = np.diff(spike_times)

    # Calculate the sampling frequency from the median time interval
    sampling_frequency = 1 / np.median(time_intervals)

    # Calculate the Nyquist frequency
    nyquist_frequency = sampling_frequency / 2

    # Calculate the maximum frequency in the FFT output
    max_frequency = 1 / (2 * np.median(time_intervals))

    # Check if the maximum frequency is greater than the Nyquist frequency
    if max_frequency > nyquist_frequency:
        print("Warning: time intervals are too small compared to sampling frequency for FFT")
        return None, None
    else:
        print("Time intervals are suitable for FFT")

    # Pad the spike times array with zeros to the nearest power of two
    n = int(2 ** np.ceil(np.log2(len(spike_times))))
    spike_times_padded = np.zeros(n)
    spike_times_padded[:len(spike_times)] = spike_times

    # Calculate the FFT of the padded spike times array
    spike_fft = np.fft.fft(spike_times_padded)

    # Calculate the frequency values for the FFT output
    freqs = np.fft.fftfreq(len(spike_times_padded)) * sampling_frequency
    return freqs, spike_fft



# Pad the spike times array with zeros to the nearest power of two
n = int(2 ** np.ceil(np.log2(len(spike_times))))
spike_times_padded = np.zeros(n)
spike_times_padded[:len(spike_times)] = spike_times

# Calculate the FFT of the padded spike times array
spike_fft = np.fft.fft(spike_times_padded)

# Calculate the frequency values for the FFT output
freqs = np.fft.fftfreq(len(spike_times_padded)) * sampling_frequency

# Plot the FFT output
plt.plot(freqs, np.abs(spike_fft))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.show()



# df1 = data.df_sorted
# df_e = df1[df1['event'].isin(eating_events)]
# df_s = df1[df1['event'].isin(['Spont', 'spont'])]
# df_w = df1[(df1.index <= df_e.index[0]) & (df1['event'].isin(well_events))]
#
# uni = data.df_sorted.loc[data.df_sorted.mid.drop_duplicates().index, ['neuron', 'color', 'counts', 'mid']]
#
# isi = np.diff(df_e.neuron)
# bins = np.arange(-.005, 0.2, 0.001)
# counts, _ = np.histogram(isi, bins)
# prob = counts / len(isi)
# fig, ax = plt.subplots()
# ax.bar(bins[:-1], prob, width=1e-3)
# ax.set_xlabel("ISI [s]")
# ax.set_ylabel("Frequency", fontweight='bold')
# ax.set_frame_on(False)
# plt.tight_layout()
# plt.show()
# for event, trial in data_trials.items():
#     if trial:
#         for trial_num, this_trial_df in data_trials[event].items():
#         # data_trials[event][trial]
#             single_histo(this_trial_df, 0)

# df_all_ev = pd.concat([df_spont, df_all_e, df_all_w], axis=0)
# df_all_ev = df_all_ev.drop('mid', axis=1).reset_index(drop=True)
# df_all_ev = df_all_ev.reset_index(drop=True)
#
# fig, ax = plt.subplots()
# ax.bar(df_all_ev.index, gaussian_filter(df_all_ev.counts, sigma=2), width=0.1, color=df_all_ev.color)
# ax.set_title("Everything", fontweight='bold')
# ax.axes.get_xaxis().set_visible(False)
# ax.set_ylabel("Frequency (hz)", fontweight='bold')
# ax.set_frame_on(False)
# # plt.tight_layout()
# plt.savefig(r'C:\Users\Flynn\Dropbox\Lab\fig')






