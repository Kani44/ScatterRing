import os

def txt_to_lst(filename):

    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    file_path = os.path.join(script_dir,filename)

    with open(file_path, 'r') as file:
        numbers_list = [int(line) for line in file] #conversions
    
    return numbers_list