import sys
import numpy as np
import random
import csv
import re, string
import time
import math

FGN_TEST = sys.argv[1]
R = sys.argv[2]

#Create a set of words to test other languages on
#Input: None
#Output: A set of words (10 chars long) that is based on english letter frequencies
def make_detectors(freq):
    #original frequencies from Robert Lewand's Crypotological Mathematics
    #current version
    #6-least frequent = twice as frequent as average
    #6-most frequent = half as frequent as average
    #all others = 1/26 frequency (denoted as average)

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
    for i in range(100):
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
	logsum = 0
	sum = 0
	true_sum = 0
	#for every detector, check every test point
	#calculate logsum
	for d in detectors:
		for t in test:
			s = 0
			logs = 0
			e = r
			while (e <= len(d)):
				if d[s:e] == t[s:e]:
					logs+=1
				s += 1
				e += 1
			#calculate logsum for anomaly score
			try:
				if (math.log(logs) == 0):
					logsum += .000001
				else:
					logsum += math.log(logs)
			except:
				continue

	#calculate sum & true sum
	for d in detectors:
		for t in test:
			current_sum = 0
			s = 0
			e = r
			#sliding window
			while (e <= len(d)):
				#if substring matches, anomaly score increases
				if d[s:e] == t[s:e]:
					sum += 1
					current_sum += 1
				s += 1
				e += 1
			#see if the score is a true anomaly or not
			if logsum < current_sum:
				true_sum += 1

	return sum, logsum, true_sum

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
		print d
		scores[d] = score
		sum = 0
	#Return the average of the test data
	return np.mean(scores)

def make_chiral_test():
	chiral_test = set()
	achiral_test = set()
	#regex pattern to remove all symbolx and numbers
	pattern = re.compile('[^a-zA-Z]+')
	#read through CSV file - make a set with compound and chirality
	with open("KEGGchiralityanalysis.csv") as csvfile:
		readCSV = csv.reader(csvfile)
		readCSV.next()
		readCSV.next()
		for row in readCSV:
			s = row[16]
			n = ''
			#account for multiple elements
			for i in range(len(s)):
				if i+1 < len(s) and s[i+1].isdigit():
					n = n + (s[i]*int(s[i+1]))
				else:
					n = n + s[i]
			#remove all non-letter characters
			n = pattern.sub('', n)
			if (int(row[6]) > 0):
				chiral_test.add(n)
			else:
				achiral_test.add(n)
	return chiral_test, achiral_test

def chiral_stats(chiral_detect):
	#Determine average length, max, and min length
	len_sum = 0
	min_len = 1000000
	max_len = 0
	for i in chiral_detect:
		if (len(i) < min_len):
			min_len = len(i)
		if (len(i) > max_len):
			max_len = len(i)
		len_sum += len(i)

	print "Average length is:", len_sum/len(chiral_detect)
	print "Max length is:", max_len
	print "Min length is:", min_len

def main():
	#Create english training data - reverse letter frequencies
	eng_freq = {
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
	chiral_freq = {
	'C': 12.49,
	'O': 24.99,
	'N': 24.99,
	'P': 49.99,
	'H': 0.05455
	}
	#Make detectors (with timing)
	t0 = time.time()
	eng_train = make_detectors(eng_freq)
	t1 = time.time()
	print "Letter detector time: ", t1-t0

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

	#test the training data on the test langauge
	d, logsum, true_sum = detect(eng_train, fgn_test, int(R))
	print "\n" + FGN_TEST[:-4] + " stats\n-------------------------"
	print "Raw detection:", d
	print "Logsum:", logsum
	print "True detection:", true_sum
	# kNN_score = kNN(eng_train, fgn_test)
	# print "kNN score: ", kNN_score

	#create chiral detector set
	t0 = time.time()
	chiral_detect = make_detectors(chiral_freq)
	t1 = time.time()
	print "\nChiral detector time:", t1-t0
	#create chiral test sets
	chiral_test, achiral_test = make_chiral_test()

	print "\nAchiral Stats\n-------------------------"
	chiral_stats(achiral_test)
	d, logsum, true_sum = detect(chiral_detect, random.sample(achiral_test, k=1000), int(R))
	print "Raw detection:", d
	print "Logsum:", logsum
	print "True detection:", true_sum
	# kNN_score = kNN(chiral_detect, achiral_test)
	# print "kNN score: ", kNN_score

	print "\nChiral Stats\n-------------------------"
	chiral_stats(chiral_test)
	d, logsum, true_sum = detect(chiral_detect, random.sample(chiral_test, k=1000), int(R))
	print "Raw detection:", d
	print "Logsum:", logsum
	print "True detection:", true_sum
	# kNN_score = kNN(chiral_detect, chiral_test)
	# print "kNN score: ", kNN_score

main()
