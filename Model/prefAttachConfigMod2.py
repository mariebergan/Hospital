import random
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from collections import Counter
import sys

groups = ['ADM', 'MED', 'NUR', 'PAT']

### Empirical contacts ###
tab = {}
for g1 in groups:
    tab[g1] = {}
    for g2 in groups:
        tab[g1][g2] = []

edgeList = open('Data/edgeList.txt')
next(edgeList)
for line in edgeList:
    splitLine = line.rstrip().split('\t')
    i = int(splitLine[0])
    j = int(splitLine[1])
    Si = splitLine[2]
    Sj = splitLine[3]
    tab[Si][Sj].append(i)
    tab[Sj][Si].append(j)
edgeList.close()

empDegrees = {}
for g1 in groups:
    empDegrees[g1] = {}
    for g2 in groups:
        occurences = Counter(tab[g1][g2])
        empDegrees[g1][g2] = list(occurences.values())
        # add nodes with k = 0
        if g1 == 'ADM' and len(empDegrees['ADM'][g2]) < 8:
            empDegrees['ADM'][g2].extend([0 for i in range(8-len(empDegrees['ADM'][g2]))])
        if g1 == 'MED' and len(empDegrees['MED'][g2]) < 11:
            empDegrees['MED'][g2].extend([0 for i in range(11-len(empDegrees['MED'][g2]))])
        if g1 == 'NUR' and len(empDegrees['NUR'][g2]) < 27:
            empDegrees['NUR'][g2].extend([0 for i in range(27-len(empDegrees['NUR'][g2]))])
        if g1 == 'PAT' and len(empDegrees['PAT'][g2]) < 29:
            empDegrees['PAT'][g2].extend([0 for i in range(29-len(empDegrees['PAT'][g2]))])
        empDegrees[g1][g2].sort()
#################

# Getting number of contacts actually created between a node and each other group
def getActualContacts(i, contactsArray):
    conts = {'ADM': 0, 'MED': 0, 'NUR': 0, 'PAT': 0}
    for j in range(75):
        if j < 8:
            conts['ADM'] += contactsArray[i][j]
        elif j < 19:
            conts['MED'] += contactsArray[i][j]
        elif j < 46:
            conts['NUR'] += contactsArray[i][j]
        else:
            conts['PAT'] += contactsArray[i][j]
    return conts

grp = []
for ID in range(75):
    if ID < 8:
        grp.append('ADM')
    elif ID < 19:
        grp.append('MED')
    elif ID < 46:
        grp.append('NUR')
    else:
        grp.append('PAT')

def getGrpContacts(g1, g2, contactsArray):
    conts = {}
    for i in range(groupRange[g1][0], groupRange[g1][1]):
        conts[i] = 0
        for j in range(groupRange[g2][0], groupRange[g2][1]):
            conts[i] += contactsArray[i][j]
    return conts

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

contactsArray = np.ones((75, 75), int)
np.fill_diagonal(contactsArray, 0)

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
    counter = 0
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
        counter += 1

    # print(counter)
    # print(getGrpContacts(g1, g1, contactsArray), sum(getGrpContacts(g1, g1, contactsArray).values()))
    # print(stubs, sum(stubs.values()))
    # print('\n')
    # for ID in range(groupRange[g1][0], groupRange[g1][1]):
    #     if getActualContacts(i, contactsArray)[g1] > assignedK[ID][g1]:
    #         print(ID, g1, getActualContacts(i, contactsArray)[g1], assignedK[ID][g1])

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
                    contactsArray[i, j] += 1
                    contactsArray[j, i] += 1

# Remove 1 becuse off-diagonal was initiated with 1
for i in range(75):
    for j in range(75):
        if i != j:
            contactsArray[i][j] -= 1

dailyContactsArray = contactsArray // 4

# contArr = dailyContactsArray * 4
# diffArr = np.subtract(contactsArray, contArr)
#print(diffArr)

simDegrees = {}
for g1 in groups:
    simDegrees[g1] = {}
    for g2 in groups:
        simDegrees[g1][g2] = []
        for i in range(groupRange[g1][0], groupRange[g1][1]):
            k_i = contactsArray[i, groupRange[g2][0]:groupRange[g2][1]]
            simDegrees[g1][g2].append(sum(k_i))
            simDegrees[g1][g2].sort()
                

            # for ID in range(groupRange[g1][0], groupRange[g1][1]):
            #     if getActualContacts(i, contactsArray)[g2] > assignedK[ID][g2]:
            #         print(ID, g1, g2, getActualContacts(i, contactsArray)[g2], assignedK[ID][g2])
            # for ID in range(groupRange[g2][0], groupRange[g2][1]):
            #     if getActualContacts(i, contactsArray)[g1] > assignedK[ID][g1]:
            #         print(ID, g2, g1, getActualContacts(i, contactsArray)[g1], assignedK[ID][g1])


actConts = {}
for i in range(75):
    actConts[i] = getActualContacts(i, contactsArray)
    #print(assignedK[i], actConts[i], '\t', sum(assignedK[i].values()), '\t', sum(actConts[i].values()))

def dist(g1, g2):
    x = []
    n = groupSizes[g1]
    a = params[g1][g2][0]
    b = params[g1][g2][1]
    for i in range(n):
        y = random.random()
        if g1 == 'MED' and g2 == 'MED':
            x.append(distFunctions(g1, g1)(g1))
        else:
            x.append(distFunctions(g1, g2)(y, a, b))
    return x

# def plotDist(g1, g2):
#     x = dist(g1, g2)
#     x.sort()
#     y = []
#     n = groupSizes[g1]
#     for i in range(n):
#         y.append(1-float(i)/float(n))
#     return x, y

def plotDist(g1, g2, empDist):
    x = empDist[g1][g2]
    x.sort()
    y = []
    n = groupSizes[g1]
    for i in range(n):
        y.append(1-float(i)/float(n))
    return x, y

# Heatmap
contactsArrayBkp = contactsArray
contactsArray = contactsArray+1
contactsArray = np.log(contactsArray)
config_hm = sns.heatmap(contactsArray, vmin = 1, vmax = 8)
config_hm.set_title('Simulated heatmap')
for x in [8, 19, 46]:
    config_hm.axhline(x, linewidth = 1, color = 'w')
    config_hm.axvline(x, linewidth = 1, color = 'w')

# Cumulative degree distributions subplot
#plt.style.use('seaborn')
f,((ax1, ax2, ax3, ax4),
(ax5, ax6, ax7, ax8),
(ax9, ax10, ax11, ax12),
(ax13, ax14, ax15, ax16)) = plt.subplots(4, 4, figsize = (12, 7.5))
f.suptitle('Cumulative degree distributions', fontsize = 'x-large')
f.supylabel('Frequency')
f.supxlabel('Degree ')
axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16]
logx_axs = [ax1, ax2, ax3, ax5, ax11, ax13]
logy_axs = [ax2, ax4, ax5, ax7, ax8, ax9, ax10, ax12, ax14, ax15, ax16]
i = 0

for g1 in groups:
    for g2 in groups:
        # Empirical
        x = empDegrees[g1][g2]
        y = np.arange(len(empDegrees[g1][g2]))/float(len(empDegrees[g1][g2]))
        axs[i].plot(x, 1-y)
        # Simulated
        x2 = simDegrees[g1][g2]
        y2 = np.arange(len(simDegrees[g1][g2]))/float(len(simDegrees[g1][g2]))
        axs[i].plot(x2, 1-y2)
        # Distributions
        x3, y3 = plotDist(g1, g2, empStubs)
        axs[i].plot(x3, y3, '--')

        for ax in logx_axs:
            ax.semilogx()
        for ax in logy_axs:
            ax.semilogy()
        i += 1
f.legend(['Empirical', 'Simulated', 'Distribution'])
axs[12].set_xlabel('ADM')
axs[13].set_xlabel('MED')
axs[14].set_xlabel('NUR')
axs[15].set_xlabel('PAT')
axs[0].set_ylabel('ADM')
axs[4].set_ylabel('MED')
axs[8].set_ylabel('NUR')
axs[12].set_ylabel('PAT')
f.tight_layout()
#plt.show()
#plt.savefig('Figs/fig'+sys.argv[1]+'.png')
