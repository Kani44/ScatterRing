# run with:
# nc -l -u localhost 7356 | python3 pipe_sdr.py

import sys
from GQRXPipe import parse_signed_16bit_numbers, split_by_2
from pynput import keyboard
import time
import numpy as np


def on_press(key): #This function just later sets the code up for stopping when esc is pressed
    if key == keyboard.Key.esc:
        return False  

def in_range(num, range): #Range must be given from min to max, Self explanatory code
    return range[0] <= num <= range[1]

def read_state(state): #This function reads the 0.25 sec samples of averages and eventually outputs a real 1 or 0
    if state[0] != state[-1]: # If there has been a change in the 0.25 sec sample of 1/0
        print(state[0]) #Print the real 1/0 before the change happened
        state = [state[-1]] #Reset the list with the first element being the starting 0.25 sec one or 0
    else:                   # 4 0.25 ones or 0.25 zeroes is a real 1 or 0. The else statement just prints the 1/0 then resets the state
        if len(state) == 4:
            print(state[0])
            state = []
    return state
        

def checker(sample_time, one_range, zero_range, dataset, parsed_data, current_state):
    for piece in dataset:
        parsed_data.append(parse_signed_16bit_numbers(piece)) # This just appends numbers from GQRX into a list
        if len(parsed_data) == int(sample_time*48000):  #This checks if the number of elements in the list is what we actually want to sample
            avg = np.mean(parsed_data)        
            if in_range(avg, one_range):    # Next few lines append a 0.25 sec 1/0 depending on the average value of the previous sample
                current_state.append(1)
            elif in_range(avg, zero_range):
                current_state.append(0)
            else:
                pass
            parsed_data = []
            current_state = read_state(current_state)
    return parsed_data, current_state


sample_time = 0.25 # These values are starting constant values
one_range = [-350, -250]
zero_range = [-200, 10]
start_state = []

listener = keyboard.Listener(on_press=on_press)
listener.start()

if __name__ == '__main__':
    while True:
        data = sys.stdin.buffer.read(1024) #This is data coming in real-time
        new_data = split_by_2(data)
        start_state = checker(sample_time, one_range, zero_range, new_data, start_state)
        if not listener.is_alive(): # This executes the esc killing the code command
            break

