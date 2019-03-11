from collections import Counter

s = list("O=C1NC(N)=NC2=C1[N+]3=CN(C4=CC=C(C(NC(C(O)=O)CCC(O)=O)=O)C=C4)CC3CN2")
n = ''

for i in s:
    if i.isalpha():
        n = n+i
    elif i.isdigit():
        n = n + str(n[-1] * (int(i)-1))

print Counter(n)
