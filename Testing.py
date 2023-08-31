from pylab import *
from rtlsdr import *
import numpy as np
import matplotlib.pyplot as plt


sdr = RtlSdr()

# configure device
sdr.sample_rate = 1.8e6
sdr.center_freq = 63.98e6
sdr.gain = 0


while True:
    plt.figure()
    plt.ion()
    plt.show()
    plt.xlabel('Time (s)', fontsize = 15)
    plt.ylabel('Amplitude', fontsize = 15)
    # # use matplotlib to estimate and plot the PSD
    samples = sdr.read_samples(256*1024)
    Pxx, freqs = psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
    fig, ax = plt.subplots(1)
    ax.plot(Pxx)

    ax.set_xticks(list(range(len(Pxx))), ['%.4f'% f for f in freqs], rotation='vertical')
    
    plt.draw()
    plt.pause(0.001)

    # print(freqs)

    # xlabel('Frequency (MHz)')
    # ylabel('Relative power (dB)')

    print(min(Pxx), '...', max(Pxx))

    # # print(np.abs(samples).shape)