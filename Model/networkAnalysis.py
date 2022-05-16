import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import spearmanr
from scipy.stats import t
from matplotlib.lines import Line2D
from configurationModel import *
from empContactsArray import *

#simContactsArray = configMod()[0]


for ID in len(empContactsArray):
    print(ID)

def getK(contactsArray):
    k = {}
    i = 0
    for row in contactsArray:
        k[i] = sum(row)
        i += 1
    return k

def plotDegreeDist(empContacts, simContacts, n):
    # emp
    empK = getK(empContacts)
    x = sorted(list(empK.values()))
    y = np.arange(len(x))/float(len(x))
    plt.plot(x, 1-y)
    # sim
    for sim in range(n):
        simK = getK(simContacts)
        x2 = sorted(list(simK.values()))
        y2 = np.arange(len(x2))/float(len(x2))
        plt.plot(x2, 1-y2, 'g', alpha = 0.2)
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.legend(['Empirical', 'Simulated'], loc='upper right', frameon=False)
    #plt.semilogx()
    plt.semilogy()
    plt.title('Cumulative Degree Distribution')
    plt.savefig('wardDegreeDist_logy_20sims.png')
    plt.show()

#plotDegreeDist(empContactsArray, 20)

def getB(contactsArray):
    k = getK(contactsArray)
    B = {}
    for i in range(75):
        B[i] = 0
        for j in range(75):
            Wij = contactsArray[i][j]
            B[i] += (Wij * k[j])
    return B

def plotSumOfNeighbouredKbdist(empContacts, simContacts, n):
    # emp
    empB = getB(empContacts)
    x = sorted(list(empB.values()))
    y = np.arange(len(x))/float(len(x))
    plt.plot(x, 1-y)
    # sim
    for sim in range(n):
        print(sim)
        simB = getB(simContacts)
        x2 = sorted(list(simB.values()))
        y2 = np.arange(len(x2))/float(len(x2))
        plt.plot(x2, 1-y2, 'g', alpha = 0.2)
    # plt.semilogx()
    plt.semilogy()
    plt.legend(['Empirical', 'Simulated'], loc='upper right', frameon=False)
    plt.title('Sum of Neighboured Degrees')
    plt.savefig('sumOfNeighbouredDegrees.png')
    plt.show()

def getA(contactsArray):
    k = getK(contactsArray)
    A = {}
    for i in range(75):
        A[i] = 0
        for j in range(75):
            Wij = contactsArray[i][j]
            A[i] += (Wij * k[j])
        A[i] = (A[i] / k[i])
    return A

groups = ['ADM', 'MED', 'NUR', 'PAT']
grpRange = {'ADM': [0, 8], 'MED': [8, 19], 'NUR': [19, 46], 'PAT': [46, 75]}
grpColor = {'ADM': 'tab:blue', 'MED': 'tab:purple', 'NUR': 'tab:green', 'PAT': 'tab:orange'}

def plotAssortativity(contactsArray):
    k = getK(contactsArray)
    B = getB(contactsArray)
    x = list(k.values())
    y = list(B.values())
    rho, p = spearmanr(x, y)
    print(rho, p)
    for grp in groups:
        for i in range(grpRange[grp][0], grpRange[grp][1]):
            plt.scatter(x[i], y[i], color = grpColor[grp])
    customLines = [Line2D([0], [0], color='tab:blue'), Line2D([0], [0], color='tab:purple'), 
                   Line2D([0], [0], color='tab:green'), Line2D([0], [0], color='tab:orange')]
    plt.legend(customLines, ['ADM', 'MED', 'NUR', 'PAT'], frameon=False)
    plt.xlabel('Degree')
    plt.ylabel('Sum of neigboured degrees')
    plt.title('Degree correlations')
    # plt.semilogx()
    # plt.semilogy()
    plt.tight_layout()
    plt.savefig('empDegreeCorr.png')
    plt.show()

#plotAssortativity(empContactsArray)

def calcConfInterval(x):
    m = np.mean(x) 
    s = np.std(x) 
    dof = len(x)-1 
    confidence = 0.95
    t_crit = np.abs(t.ppf((1-confidence)/2,dof))
    confInt = [m-s*t_crit/np.sqrt(len(x)), m+s*t_crit/np.sqrt(len(x))]
    return confInt

def calculateAssortativity(n):
    rhoN = []
    for sim in range(n):
        print(sim)
        simContacts = configMod()[0]
        k = getK(simContacts)
        B = getB(simContacts)
        rho, p = spearmanr(list(k.values()), list(B.values()))
        rhoN.append(rho)
    avgRho = sum(rhoN)/n
    print(avgRho)
    return avgRho

#calculateAssortativity(3)


def heatmap(contactsArray):
    contactsArray = contactsArray+1
    contactsArray = np.log(contactsArray)
    hm = sns.heatmap(contactsArray, vmin = 1, vmax = 8)
    hm.set_title('Simulated network')
    plt.xlabel('ADM     MED                NUR                            PAT              ')
    plt.ylabel('              PAT                         NUR              MED    ADM')
    for x in [8, 19, 46]:
        hm.axhline(x, linewidth = 1, color = 'w')
        hm.axvline(x, linewidth = 1, color = 'w')
    plt.tight_layout()
    plt.savefig('simHeatmap.png')
    plt.show()

#heatmap(simContactsArray)