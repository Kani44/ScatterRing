from pylab import *
from rtlsdr import *
import numpy as np
import matplotlib.pyplot as plt
import heapq


sdr = RtlSdr()

# configure device
sdr.sample_rate = 1.8e6
sdr.center_freq = 63.98e6
sdr.gain = 0
lst1 = []
lst2 = []
x_axis = []

plt.figure(1)
plt.ion()
plt.show()
plt.ion()
plt.show()

while True:
    samples = sdr.read_samples(256*1024)

    # for i in range(1000):
    #     print(max(np.abs(sdr.read_samples(256*1024))))

    #sdr.close()
    # import scipy.signal as signal

    # f, Pxx = signal.periodogram(samples, sdr.sample_rate/1e6)
    # print(Pxx.shape)

    # plot(np.fft.fftfreq(len(samples), sdr.sample_rate) + sdr.center_freq)
    # show()

    # # use matplotlib to estimate and plot the PSD
    #Pxx, freqs = psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
    from matplotlib.mlab import psd
    Pxx, freqs = psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6)
    freqs += sdr.center_freq/1e6 

    points = dict(zip(freqs, Pxx))

    #large_bois = heapq.nlargest(10, points, key = points.get)
    #print(large_bois)

    lst1.append(points.get(63.913203124999995))
    lst2.append(points.get(64.00109375))
    x_axis.append(len(x_axis) + 1)
    #plt.figure(1)
    plt.subplot(211)
    plt.plot(x_axis, lst1, color='black')
    plt.draw()
    plt.pause(0.001)
    plt.subplot(212)
    plt.plot(x_axis, lst2, color='black')
    plt.draw()
    plt.pause(0.001)



    # fig, ax = plt.subplots(1)
    # ax.plot(Pxx)
    # ax.set_xticks(list(range(len(Pxx))), ['%.4f'% f for f in freqs], rotation='vertical')
    # plt.show()

    # print(freqs)

    # xlabel('Frequency (MHz)')
    # ylabel('Relative P (dB)')

    #print(min(Pxx), '...', max(Pxx))

    #show()

    # # print(np.abs(samples).shape)

    # while True:
    #     plt.figure()
    #     plt.ion()
    #     plt.show()
    #     # # use matplotlib to estimate and plot the PSD
    #     samples = sdr.read_samples(256*1024)
    #     Pxx, freqs = psd(samples, NFFT=1024, Fs=sdr.sample_rate/1e6, Fc=sdr.center_freq/1e6)
    #     fig, ax = plt.subplots(1)
    #     ax.plot(Pxx)

    #     ax.set_xticks(list(range(len(Pxx))), ['%.4f'% f for f in freqs], rotation='vertical')

    #     plt.draw()
    #     plt.pause(0.001)

    #     # print(freqs)

    #     # xlabel('Frequency (MHz)')
    #     # ylabel('Relative P (dB)')

    #     print(min(Pxx), '...', max(Pxx))

    #     # # print(np.abs(samples).shape)