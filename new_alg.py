# run with:
# nc -l -u localhost 7355 | python3 new_alg.py
def parse_signed_16bit_numbers(data):
    #Assuming 'data'is a 2-byte string or bytes object
    #Convert the bytes to a signed short using litte-endian format
    signed_number = struct.unpack('<h', data)[0]
    return signed_number

def split_by_2(string):
    return [string[i:i+2] for i in range(0, len(string), 2)]






class Source: 
    def __init__(self, online):
        self.online = online
        cache = []
        if online:
            pass
        else:
            pass

    def getData(self):
        if self.online:
            if len(cache) > 0:
                return cache.pop()
            else:
                data = sys.stdin.buffer.read(1024)
                new_data = split_by_2(data)
                for piece in data:
                    cache.append(parse_signed_16bit_numbers(piece))
                return cache.pop()
        else:
            pass


source = Source(True)

def collect():
    window = 0.5
    gap = 2000
    current_data = []
    current_state = []
    once = True
    while True:
        current_data.append(source.getData(True))
        if len(current_data) >= int(window*48000):
            current_data, current_state, once = process(current_data, current_state, once)


def process(data, first, state):
    med = np.median(data)
    if first:
        if (med) < 0:
            last_value = 1
            print(last_value)
            state = [med]
            first = False
        else:
            last_value = 0
            print(last_value)
            state = [med]
            first = False
    else:

                            
        if (len(state)>=2) and (abs(med-state[-2])>gap):    # Next few lines append a 0.25 sec 1/0 depending on the average value of the previous sample
            if ((last_value == 1) and ((med-state[-2]) < 0)) or ((last_value == 0) and ((med-state[-2]) > 0)):
                last_value = flip(last_value)
                state = [med]
                print(last_value)
                print(state)
            else:
                state.append(med)
                if len(state) == 5: 
                    print(last_value)
                    state = [med]
        else:
            state.append(med)
            if len(state) == 5: 
                print(last_value)
                state = [med]
                #print(state)
    data = []
    return data, state, first



 collect()           
            

