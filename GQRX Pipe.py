import socket
import struct
import sys
import time
import os


def parse_signed_16bit_numbers(data):
    #Assuming 'data'is a 2-byte string or bytes object
    #Convert the bytes to a signed short using litte-endian format
    signed_number = struct.unpack('<h', data)[0]
    return signed_number

def split_by_2(string):
    return [string[i:i+2] for i in range(0, len(string), 2)]

script_dir = os.path.dirname(__file__)
abs_file_path = os.path.join(script_dir, spec_path)

file_path1 = os.path.join(script_dir, 'output.bin')

with open(file_path1, 'r+b') as file:
    content = file.read()

file_path2 = os.path.join(script_dir, 'output.txt')

with open(file_path2, 'w') as file2:
    #Redirect the standard output to the file
    #print("Started with test " + str(trial))
    sys.stdout = file2
    new_data = split_by_2(content)
    for piece in new_data:
        print("%s" % parse_signed_16bit_numbers(piece))
    sys.stdout = sys.__stdout__