import numpy as np
import random
import matplotlib.pyplot as plt
from empContactsArray import empContactsArray

groups = ['ADM', 'MED', 'NUR', 'PAT']
groupRange = {'ADM': [0, 8], 'MED': [8, 19], 'NUR': [19, 46], 'PAT': [46, 75]}
groupSizes = {'ADM': 8, 'MED': 11, 'NUR': 27, 'PAT': 29}
gpNo = {'ADM': 0, 'MED': 1, 'NUR': 2, 'PAT': 3}

k_min = {'ADM': {'ADM': 4, 'MED': 0, 'NUR': 1, 'PAT': 0},
         'MED': {'ADM': 7, 'MED': 131, 'NUR': 23, 'PAT': 18},
         'NUR': {'ADM': 0, 'MED': 0, 'NUR': 58, 'PAT': 33},
         'PAT': {'ADM': 0, 'MED': 0, 'NUR': 0, 'PAT': 0}}

k_max = {'ADM': {'ADM': 258, 'MED': 269, 'NUR': 1096, 'PAT': 150},
         'MED': {'ADM': 174, 'MED': 1908, 'NUR': 450, 'PAT': 350},
         'NUR': {'ADM': 320, 'MED': 120, 'NUR': 3056, 'PAT': 680},
         'PAT': {'ADM': 112, 'MED': 120, 'NUR': 680, 'PAT': 60}}


params = {'ADM': {'ADM': [2, 0.3], 'MED': [1, -2.5], 'NUR': [1, 0.3], 'PAT': [0, 150]},
          'MED': {'ADM': [10, -1.1], 'MED': [0, 0], 'NUR': [0, 430], 'PAT': [0, 340]},
          'NUR': {'ADM': [0, 325], 'MED': [0, 200], 'NUR': [60, 0.6], 'PAT': [0, 610]},
          'PAT': {'ADM': [0.8, 0.5], 'MED': [0, 115], 'NUR': [0, 670], 'PAT': [0, 55]}}

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


def configMod():
    assignedK = {}
    for ID in range(75):
        assignedK[ID] = {}

    empStubs = {'ADM': {}, 'MED': {}, 'NUR': {}, 'PAT': {}}

    contacts = {}
    for i in range(75):
        contacts[i] = {}
        for j in range(75):
            if i != j:
                contacts[i][j] = 1
            else:
                contacts[i][j] = 0

    simContactsArray = np.ones((75, 75), int)
    np.fill_diagonal(simContactsArray, 0)

    # Diganoal blocks
    for g1 in groups:
        stubs = {}
        empStubs[g1][g1] = []
        for ID in range(groupRange[g1][0], groupRange[g1][1]):
            if g1 == 'MED':
                k = distFunctions(g1, g1)(g1)
            else:
                y = random.random()
                a = params[g1][g1][0]
                b = params[g1][g1][1]
                k = distFunctions(g1, g1)(y, a, b)
            stubs[ID] = k
            assignedK[ID][g1] = k
            empStubs[g1][g1].append(k)

        # Connect stubs on diagonal
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
                simContactsArray[i, j] += 1
                simContactsArray[j, i] += 1

    # Off-diagonal blocks
    for g1 in groups:
        for g2 in groups:
            if gpNo[g1] < gpNo[g2]:
                empStubs[g1][g2] = []
                empStubs[g2][g1] = []
                stubs1 = {}
                stubs2 = {}
                for ID in range(groupRange[g1][0], groupRange[g1][1]):
                    y = random.random()
                    a = params[g1][g2][0]
                    b = params[g1][g2][1]
                    k = distFunctions(g1, g2)(y, a, b)
                    stubs1[ID] = k
                    assignedK[ID][g2] = k
                    empStubs[g1][g2].append(k)
                for ID in range(groupRange[g2][0], groupRange[g2][1]):
                    y = random.random()
                    a = params[g2][g1][0]
                    b = params[g2][g1][1]
                    k = distFunctions(g2, g1)(y, a, b)
                    stubs2[ID] = k
                    assignedK[ID][g1] = k
                    empStubs[g2][g1].append(k)

                ### Remove outliers ###
                maxStubs = max(sum(stubs1.values()), sum(stubs2.values()))
                if maxStubs == stubs1:
                    maxStubs = stubs1
                    minStubs = stubs2
                    maxGroup = g1
                else:
                    maxStubs = stubs2
                    minStubs = stubs1
                    maxGroup = g2
    
                maxStubsList = sorted(list(maxStubs.values()))
                
                n = 2 # number of outliers to remove
                count = 0
                for stubs in maxStubsList:
                    if stubs > maxStubsList[-n-1]:
                        maxStubsList[count] = maxStubsList[-n-1]
                    count += 1
                random.shuffle(maxStubsList)
                
                stubsKeys = list(range(groupRange[maxGroup][0], groupRange[maxGroup][1]))
                stubsZip = zip(stubsKeys, maxStubsList)
                maxStubsDict = dict(stubsZip)              
                
                if maxStubs == stubs1:
                    stubs1 = maxStubsDict
                    stubs2 = minStubs
                else:
                    stubs1 = minStubs 
                    stubs2 = maxStubsDict 
                #######################

                # Connect stubs on off-diagonal
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

                        contacts[i][j] += 1
                        contacts[j][i] += 1
                        simContactsArray[i, j] += 1
                        simContactsArray[j, i] += 1

    # Remove 1 becuse off-diagonal was initiated with 1
    for i in range(75):
        for j in range(75):
            if i != j:
                simContactsArray[i][j] -= 1
    simDailyContactsArray = simContactsArray // 4
    return simContactsArray, simDailyContactsArray