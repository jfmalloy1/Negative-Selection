from collections import Counter

s = list("ch3n")
n = ''

for i in s:
    if i.isalpha():
        n = n+i
    else:
        n = n + str(n[-1] * (int(i)-1))

print Counter(n)
