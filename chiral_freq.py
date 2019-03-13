#chiral_freq.py

from collections import Counter
import csv
import re

#99% of all organic compounds are made of these six elements
elements= ["H", "C", "N", "O", "Ca", "P"]
total_count = Counter()

with open("KEGGchiralityanalysis.csv") as csvfile:
    readCSV = csv.reader(csvfile)
    readCSV.next()
    readCSV.next()
    for row in readCSV:
        #Row 16 contains the chiral-determining format
        s = list(row[16])
        n = ''

        #Only count the frequency if the compound is chiral (represented by row[6] being greater than 0, meaning it has at least 1 chiral center)
        if (int(row[6]) > 0):
            for i in range(len(s)):
                if s[i] in elements:
                    if i+1 < len(s) and s[i+1].isdigit():
                        n = n + (s[i]*int(s[i+1]))
                    else:
                        n = n + s[i]

        n = re.findall('[A-Z][^A-Z]*', n)
        #all_elements.append(n)
        total_count += Counter(n)

    print total_count
