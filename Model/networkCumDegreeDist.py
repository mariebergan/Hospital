import random
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from collections import Counter

degrees_emp = [12, 18, 21, 46, 61, 63, 67, 84, 90, 93, 116, 133, 149, 153, 155, 161, 163, 164, 172, 
174, 202, 228, 236, 244, 249, 281, 288, 289, 306, 322, 367, 367, 373, 389, 404, 430, 
444, 445, 446, 460, 481, 488, 603, 624, 689, 763, 802, 848, 849, 957, 1075, 1105, 1113, 
1227, 1242, 1279, 1296, 1333, 1335, 1366, 1480, 1501, 1582, 1711, 1798, 1934, 2045, 2075,
2109, 2236, 2849, 3130, 3695, 4077, 4286]

groups = ['ADM', 'MED', 'NUR', 'PAT']
gpNo = {'ADM': 0, 'MED': 1, 'NUR': 2, 'PAT': 3}

groupRange = {'ADM': [0, 8], 'MED': [8, 19], 'NUR': [19, 46], 'PAT': [46, 75]}
groupSizes = {'ADM': 8, 'MED': 11, 'NUR': 27, 'PAT': 29}

k_min = {'ADM': {'ADM': 4, 'MED': 0, 'NUR': 1, 'PAT': 0},
         'MED': {'ADM': 7, 'MED': 131, 'NUR': 23, 'PAT': 18},
         'NUR': {'ADM': 0, 'MED': 0, 'NUR': 58, 'PAT': 33},
         'PAT': {'ADM': 0, 'MED': 0, 'NUR': 0, 'PAT': 0}}

k_max = {'ADM': {'ADM': 258, 'MED': 269, 'NUR': 1096, 'PAT': 150},
         'MED': {'ADM': 174, 'MED': 1908, 'NUR': 450, 'PAT': 350},
         'NUR': {'ADM': 320, 'MED': 120, 'NUR': 3056, 'PAT': 680},
         'PAT': {'ADM': 112, 'MED': 120, 'NUR': 680, 'PAT': 60}}
            
contacts = {}
for i in range(75):
    contacts[i] = {}
    for j in range(75):
        if i != j:
            contacts[i][j] = 1
        else:
            contacts[i][j] = 0

contactsArray = np.ones((75, 75), int)
np.fill_diagonal(contactsArray, 0)

params = {'ADM': {'ADM': [0.3, 0.35], 'MED': [1, -2.5], 'NUR': [0.1, 0.35], 'PAT': [0, 30]},
          'MED': {'ADM': [1, -2.5], 'MED': [0, 0], 'NUR': [0, 430], 'PAT': [0, 350]},
          'NUR': {'ADM': [0, 325], 'MED': [0, 200], 'NUR': [5, 0.4], 'PAT': [0, 600]},
          'PAT': {'ADM': [0.5, 0.4], 'MED': [0, 115], 'NUR': [0, 680], 'PAT': [0, 53]}}

def linLin(g1):
    return int(np.random.uniform(k_min[g1][g1], k_max[g1][g1], 1))

def logLog(y, a, b):
    return int(a*y**(b))

def logLin(y, a, b):
    return int(a*10**((1-y)/b))

def linLog(y, a, b):
    return int(-b*np.log10(y))

def distFunctions(g1, g2):
    funcs = {'ADM': {'ADM': logLin, 'MED': logLog, 'NUR': logLin, 'PAT': linLog},
             'MED': {'ADM': logLog, 'MED': linLin, 'NUR': linLog, 'PAT': linLog},
             'NUR': {'ADM': linLog, 'MED': linLog, 'NUR': logLin, 'PAT': linLog},
             'PAT': {'ADM': logLin, 'MED': linLog, 'NUR': linLog, 'PAT': linLog}}
    return funcs[g1][g2]

# diagonal
for g1 in groups:
    stubs = {}
    for ID in range(groupRange[g1][0], groupRange[g1][1]):
        if g1 == 'MED':
            k = distFunctions(g1, g1)(g1)
        else:
            y = random.random()
            a = params[g1][g1][0]
            b = params[g1][g1][1]
            k = distFunctions(g1, g1)(y, a, b)
        stubs[ID] = k

    for x in range(int((sum(stubs.values()))/2)):
        p_i = []
        sumP_i = sum(stubs.values())
        for ID in stubs:
            pVal_i = stubs[ID] / sumP_i
            p_i.append(pVal_i)
        i = int(np.random.choice(a=list(stubs), size=1, p=p_i)) 
        stubs[i] -= 1
        p_j = []
        sumP_j = 0
        for ID in stubs:
            sumP_j += contacts[i][ID] * stubs[ID]
        if sumP_j != 0:
            for ID in stubs:
                pVal_j = (contacts[i][ID] * stubs[ID]) / sumP_j
                p_j.append(pVal_j)
            j = int(np.random.choice(a=list(stubs), size=1, p=p_j))
            stubs[j] -= 1
        contacts[i][j] += 1
        contacts[j][i] += 1
        contactsArray[i, j] += 1
        contactsArray[j, i] += 1 

# non-diagonal
for g1 in groups:
    for g2 in groups:
        if g1 != g2:
            stubs1 = {}
            stubs2 = {}
            for ID in range(groupRange[g1][0], groupRange[g1][1]):
                y = random.random()
                a = params[g1][g2][0]
                b = params[g1][g2][1]
                k = distFunctions(g1, g2)(y, a, b)
                stubs1[ID] = k
           
            for ID in range(groupRange[g2][0], groupRange[g2][1]):
                y = random.random()
                a = params[g1][g2][0]
                b = params[g1][g2][1]
                k = distFunctions(g1, g2)(y, a, b)
                stubs2[ID] = k

            for x in range(min(sum(stubs1.values()), sum(stubs2.values()))):
                p_i = []
                sumP_i = sum(stubs1.values())
                for ID in stubs1:
                    pVal_i = stubs1[ID] / sumP_i
                    p_i.append(pVal_i)
                i = int(np.random.choice(a=list(stubs1), size=1, p=p_i))
                stubs1[i] -= 1
                p_j = []
                sumP_j = 0
                for ID in stubs2:
                    sumP_j += contacts[i][ID] * stubs2[ID]
                if sumP_j != 0:                
                    for ID in stubs2:
                        pVal_j = (contacts[i][ID] * stubs2[ID]) / sumP_j
                        p_j.append(pVal_j)
                    j = int(np.random.choice(a=list(stubs2), size=1, p=p_j))
                    stubs2[j] -= 1     
                if gpNo[g1] < gpNo[g2]:
                    contacts[i][j] += 1
                    contacts[j][i] += 1
                    contactsArray[i, j] += 1
                    contactsArray[j, i] += 1

degrees_sim = []
for contacts in contactsArray:
    k_i = sum(contacts)
    degrees_sim.append(k_i)
degrees_sim.sort()

x = degrees_emp
y = np.arange(len(x))/float(len(x))
plt.plot(x, 1-y, label='Empirical')
x2 = degrees_sim
y2 = np.arange(len(x2))/float(len(x2))
plt.plot(x2, 1-y2, label='Simulated')
plt.legend()
plt.xlabel('Degree')
plt.ylabel('Frequency')
#plt.semilogx()
plt.semilogy()
plt.title('Cumulative degree distribution')
plt.show()