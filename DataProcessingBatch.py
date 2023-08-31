#3.7.2 32-bit (for will at least)

'''

USAGE INSTRUCTIONS

This code uses the sys.argv function to obtain input from the command line.
When the code is run, the name of this file automatically is argv[0].
Thus, after it, the arguments should be as follows:

argv[1] = the name of the files you're reading, without number or .txt
    For example, if you were to read from output1.txt to output10.txt,
    you would enter the word output as argv[1]
argv[2] = the frequency of the station the readings were taken from (eg. 101.5)
argv[3] = the first number to read from
    For example, if you were to start with output1.txt, argv[3] would be 1
argv[4] = the last number to read from
    For example, if you were to end with output10.txt, argv[4] would be 10

FULL EXAMPLE:

[whatever the run button puts in] output 101.5 1 10

Be careful if your terminal outputs extra stuff when using the run button.

'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import *
import sys
import os

#first argument after the program name is the file, second is the radio station, third is the 
rel_path = sys.argv[1]
station_frequency = float(sys.argv[2])
filestart = int(sys.argv[3])
filend = int(sys.argv[4])

for n in range(filestart,filend+1):
    name = rel_path+str(n)
    spec_path = name+".txt"
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, spec_path) # for this to work files should be in the same folder

    raw_data = []
    with open(abs_file_path, 'r') as file:
        for line in file:
            raw_data.append(float(line))
    #raw_data = [float(i) for i in data]

    #processing of data 
    sample_rate = 48000
    duration = len(raw_data)/sample_rate
    N = len(raw_data)
    time = np.linspace(0, duration, N) #x-axis time values
    time_data = raw_data
    
    print('yeah')

    #generate time domain 
    plt.plot(time, time_data)
    plt.title('Time Domain Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.savefig(script_dir + '/Images/' + name + 'timedomain.jpg') #save
    plt.show()
    plt.close()
    #plt.figure()
    print('si')

    #frequency calculations

    #frequency = station_frequency + np.linspace(0.0, sample_rate/2, int (N/2))/1000000 - sample_rate/4000000
    print('prefft')
    freq_data = rfft(time_data, next_fast_len(len(time_data)))
    print('postfft')
    y = 2/N * freq_data #[0:np.int(N/2)] #adjusted amplitude range
    y = abs(y)
    frequency = rfftfreq((2*len(y)-1), d=1.0/sample_rate)
    #frequency = fftfreq(len(freq_data), d=1.0/sample_rate)

    print('yah')

    #generate frequency domain
    fig, ax = plt.subplots()
    ax.plot(frequency, y)
    ax.ticklabel_format(useOffset=False)
    print('nice')

    # plt.plot(y) -- x axis is #samples

    plt.title('Frequency domain Signal')
    plt.xlabel('Frequency in mHz')
    plt.ylabel('Amplitude')
    plt.savefig(script_dir + '/Images/' + name + 'frequencydomain.jpg') #save
    plt.show()
    plt.close()
    #plt.figure()

    freq_data = []

    #generate full spectrogram  
 
    plt.specgram(time_data, Fs=sample_rate)
    plt.title('Spectrogram')
    plt.xlabel("TIME")
    plt.ylabel("FREQUENCY BIN")
    plt.savefig(script_dir + '/Images/' + name + 'spectrogram.jpg')
    plt.show()
    plt.close()
    #plt.figure()
    
    plt.psd(time_data, NFFT = 8192, Fs=sample_rate)
    plt.title('PSD')
    plt.xlabel("FREQUENCY")
    plt.ylabel("POWER/FREQUENCY")
    plt.savefig(script_dir + '/Images/' + name + 'psd.jpg')
    plt.close()
    #plt.figure()

    #generate truncated spectrogram
    '''
    plt.specgram(time_data, NFFT = 2048, Fs=48000)
    plt.title('Spectrogram(Zoomed)')
    plt.xlabel("TIME")
    plt.ylabel("FREQUENCY BIN")
    plt.ylim([0, 1000])
    plt.savefig(script_dir + '/Images/' + name + 'spectrogramzoomed.jpg')
    plt.close()
    plt.figure()
    '''