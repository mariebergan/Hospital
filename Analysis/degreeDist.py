from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import poisson

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
    nodeContacts = sum(contacts)
    k.append(nodeContacts)

k.sort()
print(k)
mu = sum(k)/len(k)
pmf = poisson.pmf(k, mu)
plt.plot(k, pmf)
plt.xlabel('Degree')
plt.ylabel('Probability')
plt.title('Empirical')
plt.show()