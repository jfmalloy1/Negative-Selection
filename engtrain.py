import numpy as np
import random

def main():
    #define english letter frequencies (in reverse frequency)
    #original frequencies from Robert Lewand's Crypotological Mathematics
    freq = {
    'a': 1/.08167,
    'b': 1/.01492,
    'c': 1/.02782,
    'd': 1/.04253,
    'e': 1/.12702,
    'f': 1/.02228,
    'g': 1/.02015,
    'h': 1/.06094,
    'i': 1/.06966,
    'j': 1/.00153,
    'k': 1/.00772,
    'l': 1/.04025,
    'm': 1/.02406,
    'n': 1/.06749,
    'o': 1/.07507,
    'p': 1/.01929,
    'q': 1/.00095,
    'r': 1/.05987,
    's': 1/.06327,
    't': 1/.09056,
    'u': 1/.02758,
    'v': 1/.00978,
    'w': 1/.02360,
    'x': 1/.00150,
    'y': 1/.01974,
    'z': 1/.00074
    }
    sum = 0
    for l,f in freq.iteritems():
        sum += f
    for l,f in freq.items():
        freq[l] = f/sum

    #lists of all frequences (cumulative sum) and letters
    fs = np.cumsum(freq.values())
    ls = freq.keys()

    #make reverse English test data
    test = []
    for i in range(1000):
        s = ""
        for i in range(10):
            r = random.uniform(0, 1)
            gc = np.extract(fs > r, fs)
            element = fs.tolist().index(gc[0])
            s += ls[element]
        test.append(s)
    print test

main()
