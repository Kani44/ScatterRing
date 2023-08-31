#3.7.2 32-bit (for will at least)

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import *
import sys
import os
from scipy.signal import stft, find_peaks
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('name', type=str)
parser.add_argument('-i', type=int)
parser.add_argument('--save', action='store_true')

args = parser.parse_args()
name = args.name
indexx = args.i
save = args.save
    
spec_path = name+".txt"
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
abs_file_path = os.path.join(script_dir, spec_path) # for this to work files should be in the same folder

raw_data = []
with open(abs_file_path, 'r') as file:
    for line in file:
        raw_data.append(float(line))

#processing of data 
sample_rate = 48000
duration = len(raw_data)/sample_rate
N = len(raw_data)
time = np.linspace(0, duration, N) #x-axis time values
time_data = raw_data

#generate time domain 
plt.plot(time, time_data)
plt.title('Time Domain Signal')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.show()
plt.savefig(script_dir + '/Images/' + name + 'timedomain.jpg') #save
plt.close()


#frequency calculations

print('prefft')
#freq_data = rfft(time_data, next_fast_len(len(time_data)))
f, t, Zxx = stft(time_data, fs=sample_rate, nperseg=2048)
print('postfft')
#y = 2/N * freq_data
#y = abs(y)
#frequency = rfftfreq((2*len(y)-1), d=1.0/sample_rate)
#plt.pcolormesh(t, f, np.abs(Zxx))
#plt.plot(np.abs(Zxx))
#plt.show()
Z = [np.mean(x) for x in abs(Zxx)]
plt.plot(Z)
indices = find_peaks(Z)[0]
print(indices)
indexs = [Z[x] for x in indices]
plt.scatter(indices, indexs, color='red')
plt.savefig(script_dir + '/Images/' + name + 'Peaks.jpg')
plt.show()
plt.plot(abs(Zxx)[indexx])
plt.show()
if save:
    with open(r"C:\Users\ubicomplab\Downloads\sdrdataread\filename.txt", 'w') as file:
        list = abs(Zxx)[indexx]
        for index, line in enumerate(list):
            if index == len(list) - 1:
                file.write(str(line))
            else:
                file.write(str(line)+'\n')
    print(len(Zxx))

'''
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(
    y=Z,
    mode='lines+markers',
    name='Original Plot'
))

fig.add_trace(go.Scatter(
    x=indices,
    y=[Z[j] for j in indices],
    mode='markers',
    marker=dict(
        size=8,
        color='red',
        symbol='cross'
    ),
    name='Detected Peaks'
))

fig.show()

'''

#print(find_peaks(Z)[0])



#plt.plot(Z)
'''
plt.plot(abs(Zxx)[16])
plt.show()
plt.plot(abs(Zxx)[26])
plt.show()
plt.plot(abs(Zxx)[80])
plt.show()
'''

'''

#generate frequency domain
fig, ax = plt.subplots()
ax.plot(frequency, y)
ax.ticklabel_format(useOffset=False)

# plt.plot(y) -- x axis is #samples

plt.title('Frequency domain Signal')
plt.xlabel('Frequency in mHz')
plt.ylabel('Amplitude')
plt.savefig(script_dir + '/Images/' + name + 'frequencydomain.jpg') #save
plt.show()
plt.close()
#plt.figure()

'''