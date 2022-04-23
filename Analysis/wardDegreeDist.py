from matplotlib import pyplot as plt
import numpy as np

contactsArray = np.zeros((76,76), int)
edgeList = open('Data/edgeList.txt')
next(edgeList)
for line in edgeList:
    splitLine = line.rstrip().split('\t')
    i = int(splitLine[0])
    j = int(splitLine[1])
    Si = splitLine[2]
    Sj = splitLine[3]
    contactsArray[i][j] += 1
    contactsArray[j][i] += 1
edgeList.close()

contactsArray = contactsArray[1:76, 1:76]
k = []
for contacts in contactsArray:
    k_i = sum(contacts)
    k.append(k_i)
k.sort()

x = k
y = np.arange(len(x))/float(len(x))
plt.plot(x, 1-y)
plt.xlabel('Degree')
plt.ylabel('Frequency')
#plt.semilogx()
plt.semilogy()
plt.title('Cumulative degree distribution')
plt.show()