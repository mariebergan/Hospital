import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import scipy.stats as st
from matplotlib.lines import Line2D
from configurationModel import configMod
from empContacts import empContactsArray, empDailyContactArrays

#simContactsArray = configMod()[0]

groups = ['ADM', 'MED', 'NUR', 'PAT']
grpRange = {'ADM': [0, 8], 'MED': [8, 19], 'NUR': [19, 46], 'PAT': [46, 75]}

def getDegrees(contactsArray):
    degrees = {}
    for g1 in groups:
        degrees[g1] = {}
        for g2 in groups:
            degrees[g1][g2] = []
            for i in range(grpRange[g1][0], grpRange[g1][1]):
                k_i = contactsArray[i, grpRange[g2][0]:grpRange[g2][1]]
                degrees[g1][g2].append(sum(k_i))
                degrees[g1][g2].sort()
    return degrees

def plotBlockDegreeDist(sims):
    plt.style.use('seaborn')
    f,((ax1, ax2, ax3, ax4),
    (ax5, ax6, ax7, ax8),
    (ax9, ax10, ax11, ax12),
    (ax13, ax14, ax15, ax16)) = plt.subplots(4, 4, figsize = (10, 7.5))
    #f.suptitle('Cumulative degree distributions', fontsize = 'x-large')
    
    axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16]
    logx_axs = [ax1, ax2, ax3, ax5, ax11, ax13]
    logy_axs = [ax2, ax4, ax5, ax7, ax8, ax9, ax10, ax12, ax14, ax15, ax16]
     # Empirical
    i = 0
    for g1 in groups:
        for g2 in groups:
            empDegrees = getDegrees(empContactsArray)
            x = empDegrees[g1][g2]
            y = np.arange(len(empDegrees[g1][g2]))/float(len(empDegrees[g1][g2]))
            axs[i].plot(x, 1-y)
            i += 1
    # Simulated
    for n in range(sims):
        print(n)
        simContactsArray = configMod()[0]
        simDegrees = getDegrees(simContactsArray)
        i = 0
        for g1 in groups:
            for g2 in groups:
                x2 = simDegrees[g1][g2]
                y2 = np.arange(len(simDegrees[g1][g2]))/float(len(simDegrees[g1][g2]))
                axs[i].plot(x2, 1-y2, 'g', alpha = 0.15)
                i += 1
    for ax in logx_axs:
        ax.semilogx()
    for ax in logy_axs:
        ax.semilogy()
                
    f.legend(['Empirical', 'Simulation'], frameon=False, loc='upper right',  bbox_to_anchor=(1.0, 1.03), ncol=2)
    axs[12].set_xlabel('ADM')
    axs[13].set_xlabel('MED')
    axs[14].set_xlabel('NUR')
    axs[15].set_xlabel('PAT')
    axs[0].set_ylabel('ADM')
    axs[4].set_ylabel('MED')
    axs[8].set_ylabel('NUR')
    axs[12].set_ylabel('PAT')
    f.supylabel('             Frequency')
    f.supxlabel('                  Degree')
    f.tight_layout()
    plt.savefig('simBlockDegreeDist_10sims.png', bbox_inches='tight')
    plt.show()

    
def getK(contactsArray):
    k = {}
    i = 0
    for row in contactsArray:
        k[i] = sum(row)
        i += 1
    return k

def plotWardDegreeDist(n):
    # emp
    empK = getK(empContactsArray)
    x = sorted(list(empK.values()))
    y = np.arange(len(x))/float(len(x))
    plt.plot(x, 1-y)
    # sim
    for sim in range(n):
        print(sim)
        simContactsArray = configMod()[0]
        simK = getK(simContactsArray)
        x2 = sorted(list(simK.values()))
        y2 = np.arange(len(x2))/float(len(x2))
        plt.plot(x2, 1-y2, 'g', alpha = 0.15)
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.legend(['Empirical', 'Simulated'], loc='upper right', frameon=False)
    # plt.semilogx()
    plt.semilogy()
    #plt.title('Cumulative Degree Distribution')
    plt.tight_layout()
    plt.savefig('wardDegreeDist_20sims.png')
    plt.show()

def getB(contactsArray):
    k = getK(contactsArray)
    B = {}
    for i in range(75):
        B[i] = 0
        for j in range(75):
            Wij = contactsArray[i][j]
            B[i] += (Wij * k[j])
    return B

def plotSumOfNeighbouredKdist(n):
    # emp
    empB = getB(empContactsArray)
    x = sorted(list(empB.values()))
    y = np.arange(len(x))/float(len(x))
    # y = sorted(list(empB.values()))
    # empK = getK(empContactsArray)
    # x = sorted(list(empK.values()))
    plt.plot(x, 1-y)
    # sim
    for sim in range(n):
        print(sim)
        simContactsArray = configMod()[0]
        simB = getB(simContactsArray)
        x2 = sorted(list(simB.values()))
        y2 = np.arange(len(x2))/float(len(x2))
        # y2 = sorted(list(simB.values()))
        # simK = getK(simContactsArray)
        # x2 = sorted(list(simK.values()))
        plt.plot(x2, 1-y2, 'g', alpha = 0.2)
    # plt.semilogx()
    plt.semilogy()
    plt.xlabel('Degree')
    plt.ylabel('Sum of neighboured degree')
    plt.legend(['Empirical', 'Simulated'], loc='upper right', frameon=False)
    plt.savefig('sumOfNeighbouredDegrees_20sims.png')
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

grpColor = {'ADM': 'tab:blue', 'MED': 'tab:purple', 'NUR': 'tab:green', 'PAT': 'tab:orange'}

def calculateEmpDegreeCorr(contactsArray):
    k = getK(contactsArray)
    A = getA(contactsArray)
    k = list(k.values())
    A = list(A.values())
    grpK = {}
    grpA = {}
    for grp in groups:
        grpK[grp] = []
        grpA[grp] = []
        for i in range(grpRange[grp][0], grpRange[grp][1]):
            grpK[grp].append(k[i])
            grpA[grp].append(A[i])
        rho, p = st.spearmanr(grpK[grp], grpA[grp])
    
def plotGrpDegreeCorrelations(contactsArray):
    k = getK(contactsArray)
    A = getA(contactsArray)
    x = list(k.values())
    y = list(A.values())
    f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=True, sharey=True)
    ax = {'ADM': ax1, 'MED': ax2, 'NUR': ax3, 'PAT': ax4}
    for grp in groups:
        for i in range(grpRange[grp][0], grpRange[grp][1]):
            ax[grp].scatter(x[i], y[i], color = grpColor[grp])
        ax[grp].set_title(grp)

    # f.suptitle('Degree correlations')
    f.supxlabel('               Degree')
    f.supylabel('           Average degree of neighbours')
    plt.tight_layout()
    plt.savefig('empGrpDegreeCorr.png')
    plt.show()

def plotWardDegreeCorrelations(contactsArray):
    k = getK(contactsArray)
    A = getA(contactsArray)
    x = list(k.values())
    y = list(A.values())
    rho, p = st.spearmanr(x, y)
    for grp in groups:
        for i in range(grpRange[grp][0], grpRange[grp][1]):
            plt.scatter(x[i], y[i], color = grpColor[grp])
    customLines = [Line2D([0], [0], color='tab:blue'), Line2D([0], [0], color='tab:purple'), 
                   Line2D([0], [0], color='tab:green'), Line2D([0], [0], color='tab:orange')]
    plt.legend(customLines, ['ADM', 'MED', 'NUR', 'PAT'], frameon=False)
    plt.xlabel('Degree')
    plt.ylabel('Average degree of neighbours')
    plt.tight_layout()
    plt.savefig('empWardDegreeCorr.png')
    plt.show()

def calcSimTotalDegreeCorr(n):
    rhoN = []
    for sim in range(n):
        simContacts = configMod()[0]
        k = getK(simContacts)
        A = getA(simContacts)
        rho, p = st.spearmanr(list(k.values()), list(A.values()))
        rhoN.append(rho)
    avgRho = sum(rhoN)/n
    # confidence interval
    confInt = st.norm.interval(alpha=0.95, loc=np.mean(rhoN), scale=st.sem(rhoN))
    return avgRho, confInt

#calcSimTotalDegreeCorr(100)

def calcSimGrpDegreeCorr(n):
    rhoSim = {'ADM': [], 'MED': [], 'NUR': [], 'PAT': []}
    for sim in range(n):
        simContactsArray = configMod()[0]
        k = getK(simContactsArray)
        A = getA(simContactsArray)
        k = list(k.values())
        A = list(A.values())
        grpK = {}
        grpA = {}
        for grp in groups:
            grpK[grp] = []
            grpA[grp] = []
            for i in range(grpRange[grp][0], grpRange[grp][1]):
                grpK[grp].append(k[i])
                grpA[grp].append(A[i])
            rho, p = st.spearmanr(grpK[grp], grpA[grp])
            rhoSim[grp].append(rho)
    for grp in rhoSim:
        avgRho = sum(rhoSim[grp])/n
        confInt = st.norm.interval(alpha=0.95, loc=np.mean(rhoSim[grp]), scale=st.sem(rhoSim[grp]))

def AvgHeatmap(sims):
    contactsArray = np.zeros((75, 75), dtype = float)
    for sim in range(sims):
        print(sim)
        simArr = configMod()[0]
        for i in range(75):
            for j in range(75):
                contactsArray[i, j] += simArr[i, j]
    for i in range(75):
        for j in range(75):
            contactsArray[i, j] /= sims

    contactsArray = contactsArray+1
    contactsArray = np.log(contactsArray)

    w = []
    for i in contactsArray:
        for j in i:
            w.append(j)
    print(min(w), max(w))

    hm = sns.heatmap(contactsArray, vmin = 1, vmax = 8)
    plt.xlabel('ADM      MED                    NUR                                PAT                ')
    plt.ylabel('             PAT                            NUR                 MED    ADM')
    for x in [8, 19, 46]:
        hm.axhline(x, linewidth = 1, color = 'w')
        hm.axvline(x, linewidth = 1, color = 'w')
    plt.tight_layout()
    plt.savefig('simHeatmap.png')
    plt.show()

def heatmap():
    emp = empContactsArray+1
    sim = configMod()[0]+1
    empArr = np.log(emp)
    simArr = np.log(sim)

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5), sharey=True, sharex=True, gridspec_kw={'width_ratios': [3.2, 4]})

    empHM = sns.heatmap(empArr, ax=ax1, vmin=1, vmax=8, cbar=False)
    simHM = sns.heatmap(simArr, ax=ax2, vmin=1, vmax=8)

    ax1.set_xlabel('ADM     MED                NUR                             PAT              ')ZZ
    ax1.set_ylabel('              PAT                           NUR              MED     ADM')
    ax2.set_xlabel('ADM     MED                NUR                             PAT              ')
    ax1.set_title('Empirical')
    ax2.set_title('Simulated')
    for x in [8, 19, 46]:
            empHM.axhline(x, linewidth = 1, color = 'w')
            empHM.axvline(x, linewidth = 1, color = 'w')
            simHM.axhline(x, linewidth = 1, color = 'w')
            simHM.axvline(x, linewidth = 1, color = 'w')
    plt.tight_layout
    plt.savefig('emp_sim_heatmap.png')
    plt.show()

heatmap()



