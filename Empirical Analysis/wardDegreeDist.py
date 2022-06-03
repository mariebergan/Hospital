from matplotlib import pyplot as plt
import numpy as np

contactsArray = np.zeros((75,75), int)
edgeList = open('Data/edgeList.txt')
for line in edgeList:
    splitLine = line.rstrip().split('\t')
    i = int(splitLine[0])
    j = int(splitLine[1])
    Si = splitLine[2]
    Sj = splitLine[3]
    contactsArray[i][j] += 1
    contactsArray[j][i] += 1
edgeList.close()

def plotDegreeDist():
    k = []
    for row in contactsArray:
        k_i = sum(row)
        k.append(k_i)
    k.sort()
    x = k
    y = np.arange(len(x))/float(len(x))
    plt.plot(x, 1-y)
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    #plt.semilogx()
    plt.semilogy()
    #plt.title('Cumulative degree distribution')
    plt.savefig('/Users/marie/Documents/Utdanning/Bioteknologi master/MASTER/completeFigs/empWardDegreeDist.png')
    plt.show()

plotDegreeDist()

k = {}
i = 0
for row in contactsArray:
    k[i] = sum(row)
    i += 1

B = {}
for i in range(75):
    B[i] = 0
    for j in range(75):
        Wij = contactsArray[i][j]
        B[i] += (Wij * k[j])

x = sorted(list(B.values()))
y = np.arange(len(x))/float(len(x))
plt.plot(x, 1-y)
#plt.semilogx()
#plt.semilogy()
#plt.show()