import sys
import numpy as np
import random

FGN_TEST = sys.argv[1]
R = sys.argv[2]

#Create a set of words to test other languages on
#Input: None
#Output: A set of words (10 chars long) that is based on english letter frequencies
def engtrain():
    #original frequencies from Robert Lewand's Crypotological Mathematics
    #current version
        #6-least frequent = twice as frequent as average
        #6-most frequent = half as frequent as average
        #all others = 1/26 frequency (denoted as average)
    freq = {
    'a': .01923,
    'b': .03846,
    'c': .03846,
    'd': .03846,
    'e': .01923,
    'f': .03846,
    'g': .03846,
    'h': .03846,
    'i': .01923,
    'j': .07692,
    'k': .07692,
    'l': .03846,
    'm': .03846,
    'n': .01923,
    'o': .01923,
    'p': .03846,
    'q': .07692,
    'r': .03846,
    's': .03846,
    't': .01923,
    'u': .03846,
    'v': .07692,
    'w': .03846,
    'x': .07692,
    'y': .03846,
    'z': .07692
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
    return test

#test to evaluate response to each dector: r-contig
#input: detector set, test set
#output: frequency of detection
def detect(detectors, test, r):
    sum = 0
    for d in detectors:
        for t in test:
            s = 0
            e = r
            while (e <= len(d)):
                #print d[s:e]
                if d[s:e] == t[s:e]:
                    sum += 1
                s += 1
                e += 1
    return sum

# Dynamic Programming implementation of LCS problem
def lcs(X, Y):
	# find the length of the strings
	m = len(X)
	n = len(Y)

	# declaring the array for storing the dp values
	L = [[None]*(n + 1) for i in xrange(m + 1)]

	"""Following steps build L[m + 1][n + 1] in bottom up fashion
	Note: L[i][j] contains length of LCS of X[0..i-1]
	and Y[0..j-1]"""
	for i in range(m + 1):
		for j in range(n + 1):
			if i == 0 or j == 0 :
				L[i][j] = 0
			elif X[i-1] == Y[j-1]:
				L[i][j] = L[i-1][j-1]+1
			else:
				L[i][j] = max(L[i-1][j], L[i][j-1])

	# L[m][n] contains the length of LCS of X[0..n-1] & Y[0..m-1]
	return L[m][n]
	# This code is contributed by Nikhil Kumar Singh(nickzuck_007) from geeksforgeeks.org

#kNN code
#Inputs: detectors (training set) and test data
#Outputs: the kNN score for the particular test data
def kNN(detectors, test):
	sum = 0
	print "kNN Analysis: "
	#individual kNN scores
	scores = np.empty(len(detectors))
	#Loop through each training & test sequence
	for d in range(len(detectors)):
		for t in test:
			sum += lcs(detectors[d], t)
		#kNN score
		score = (float(sum) / len(test)) / 10
		if (d % 50 == 0 ):
			print str(float(d)/len(detectors)) + "% "
		scores[d] = score
		sum = 0
	#Return the average of the test data
	return np.mean(scores)

def main():
	#Create english training data - reverse letter frequencies
	#TODO: add underscores?
	eng_train = engtrain()

	#Read in english test data
	f = open("english.test", "r")
	test = set()
	for line in f:
		test.add(line.rstrip())
	f.close()

	#Read in foreign language test data
	f = open(FGN_TEST, "r")
	fgn_test = set()
	for line in f:
		fgn_test.add(line.rstrip())
	f.close()

	#test the training data on the foreign langauge
	d = detect(eng_train, fgn_test, int(R))
	print "Detection number:", d
	kNN_score = kNN(eng_train, fgn_test)
	print "kNN score: ", kNN_score

main()
