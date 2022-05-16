from operator import ne
import numpy as np
import seaborn as sns
from modelFuncs_seedNode import *
from InitializeParams import *
import matplotlib.pyplot as plt
from prefAttachConfigMod2 import simDailyContactsArray
from empContactsArray import empDailyContactArrays
from collections import Counter
from matplotlib.lines import Line2D


startDay = 0
runDays = 60

def runEmp(contactsArray, seedNode, seedState):
    attrs = initModel(contactsArray, baseP, seedNode, seedState)
    stateLog, infIDs, infBySeedNode = timedRun_emp(contactsArray, attrs, baseP, startDay, runDays, seedNode)
    return stateLog, infIDs, infBySeedNode
    
def runSim(contactsArray, seedNode, seedState):
    attrs = initModel(contactsArray, baseP, seedNode, seedState)
    stateLog, infIDs, infBySeedNode = timedRun_sim(contactsArray, attrs, baseP, startDay, runDays, seedNode)
    return stateLog, infIDs, infBySeedNode

def seedNodeHeatmap(runEmp, empContacts, runSim, simContacts, sims):
    empSeedInfArr = np.zeros((75, 75), dtype=int)
    simSeedInfArr = np.zeros((75, 75), dtype=int)

    for i in range(75):
        for sim in range(sims):
            print(i, sim)
            empInfIDs = runEmp(empContacts, i, 'Ip')[1]
            simInfIDs = runSim(simContacts, i, 'Ip')[1]
            for j in empInfIDs:
                empSeedInfArr[i][j] += 1
            for j in simInfIDs:
                simSeedInfArr[i][j] += 1

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4), sharey=True, sharex=True)
    empHM = sns.heatmap(empSeedInfArr, ax=ax1, vmin=0, vmax=sims)
    simHM = sns.heatmap(simSeedInfArr, ax=ax2, vmin=0, vmax=sims)
    for x in [8, 19, 46]:
            empHM.axhline(x, linewidth = 1, color = 'w')
            empHM.axvline(x, linewidth = 1, color = 'w')
            simHM.axhline(x, linewidth = 1, color = 'w')
            simHM.axvline(x, linewidth = 1, color = 'w')
    ax1.set_xlabel('ADM   MED              NUR                          PAT            ')
    ax2.set_xlabel('ADM   MED              NUR                          PAT            ')
    ax1.set_ylabel('               PAT               NUR          MED  ADM')
    ax1.set_title('Empirical')
    ax2.set_title('Simulated')
    f.tight_layout()
    plt.savefig('testSeedNode_p0.001.png')
    plt.show()

seedNodeHeatmap(runEmp, empDailyContactArrays, runSim, simDailyContactsArray, 100)

groups = ['ADM', 'MED', 'NUR', 'PAT']
groupRange = {'ADM': [0, 7], 'MED': [8, 18], 'NUR': [19, 45], 'PAT': [46, 74]}

def getInfBySeedNode(runModel, contactsArray, sims):
    infBySeedNode = {} 
    for grp in groups:
        infBySeedNode[grp] = {'Ia' : [], 'Ip' : []}
        stateInf = {'Ia' : [], 'Ip' : []}
        for sim in range(sims):
            for seedState in {'Ia', 'Ip'}:
                seedNode = random.randint(groupRange[grp][0], groupRange[grp][1]) 
                infs = runModel(contactsArray, seedNode, seedState)[2]
                stateInf[seedState].append(infs)
        stateInf['Ia'].sort()
        stateInf['Ip'].sort()
        infBySeedNode[grp]['Ia'] = dict(Counter(stateInf['Ia']))
        infBySeedNode[grp]['Ip'] = dict(Counter(stateInf['Ip']))

    return infBySeedNode

def aggregateAbove6(infBySeedNode):
    infBySeedNode_aggr = {}
    for grp in groups:
        infBySeedNode_aggr[grp] = {'Ia' : {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, '>6':0}, 'Ip' : {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, '>6':0}}
        for seedState in {'Ia', 'Ip'}:
            for n in infBySeedNode[grp][seedState]: 
                if n in range(7):
                    infBySeedNode_aggr[grp][seedState][n] += infBySeedNode[grp][seedState][n]
                else:
                    infBySeedNode_aggr[grp][seedState]['>6'] += infBySeedNode[grp][seedState][n]
    return infBySeedNode_aggr

def calculateR0(infBySeedNode, sims):
    R0 = {}
    for grp in groups:
        R0[grp] = {'Ia' : 0, 'Ip' : 0} 
        for seedState in R0[grp]:     
            R = []
            for nInf in infBySeedNode[grp][seedState]:
                r = nInf * (infBySeedNode[grp][seedState][nInf]/sims)
                R.append(r)
            R0[grp][seedState] = round(sum(R), 2)
    return R0

def plotR(runEmp, empContacts, runSim, simContacts, sims):
    infBySeedNode_emp = getInfBySeedNode(runEmp, empContacts, sims)
    infBySeedNode_sim = getInfBySeedNode(runSim, simContacts, sims)
    infBySeedNode_aggr_emp = aggregateAbove6(infBySeedNode_emp)
    infBySeedNode_aggr_sim = aggregateAbove6(infBySeedNode_sim)
    R0_emp = calculateR0(infBySeedNode_emp, sims)
    R0_sim = calculateR0(infBySeedNode_sim, sims)
    networks = ['emp', 'sim']

    f,((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8),
        (ax9, ax10, ax11, ax12), (ax13, ax14, ax15, ax16) ) = plt.subplots(4, 4, figsize=(8, 8))
    axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16]

    i = 0
    for grp in groups:
        for seedState in infBySeedNode_emp[grp]:
                for network in networks:
                    if network == 'emp':
                        x = list(infBySeedNode_aggr_emp[grp][seedState].values())
                        mylabels = list(infBySeedNode_aggr_emp[grp][seedState])
                        axs[i].pie(x)
                        axs[i].set_xlabel(r'$R_0$ = ' + str(R0_emp[grp][seedState]))
                    else:
                        x = list(infBySeedNode_aggr_sim[grp][seedState].values())
                        axs[i].pie(x)
                        axs[i].set_xlabel(r'$R_0$ = ' + str(R0_sim[grp][seedState])) 
    
                    print(i)
                    i += 1

    f.legend(labels=mylabels, frameon=False, loc='upper center',  bbox_to_anchor=(1.03, 1.0))
    f.suptitle('          Asymptomatic                                              Presymptomatic')
    ax1.set_title('Empirical', fontsize=10)
    ax2.set_title('Simulated', fontsize=10)
    ax3.set_title('Empirical', fontsize=10)
    ax4.set_title('Simulated', fontsize=10)
    ax1.set_ylabel('ADM          ', rotation='horizontal')
    ax5.set_ylabel('MED          ', rotation='horizontal')
    ax9.set_ylabel('NUR          ', rotation='horizontal')
    ax13.set_ylabel('PAT          ', rotation='horizontal')
    f.tight_layout()
    plt.savefig('R0pieChart_p0.0005.png', bbox_inches='tight')
    plt.show()

#plotR(runEmp, empDailyContactArrays, runSim, simDailyContactsArray, 100) 

def plot_p_R0():
    p = [0.0005, 0.001, 0.005, 0.01]
    asympR0 = {'emp': {'ADM': [0.18, 0.27, 1.2, 1.89], 'MED': [0.36, 0.86, 2.9, 4.86], 'NUR': [0.38, 0.55, 2.98, 4.87], 'PAT': [0.11, 0.11, 0.98, 1.37]},
               'sim': {'ADM': [0.17, 0.85, 1.16, 1.24], 'MED': [0.27, 0.56, 3.4, 4.7], 'NUR': [0.31, 0.55, 2.21, 4.65], 'PAT': [0.11, 0.12, 0.73, 1.21]}}

    presympR0 = {'emp': {'ADM': [0.8, 0.84, 3.97, 6.41], 'MED': [1.4, 2.36, 8.26, 10.25], 'NUR': [1.11, 3.15, 7.84, 11.3], 'PAT': [0.32, 0.64, 2.69, 4.26]},
               'sim': {'ADM': [0.72, 1.9, 3.24, 3.08], 'MED': [1.14, 1.84, 7.15, 9.55], 'NUR': [1.25, 2.08, 4.95, 11.49], 'PAT': [0.37, 0.42, 2.35, 2.9]}}
    
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    styles = {'emp': {'ADM': ['tab:blue', '-'], 'MED': ['tab:purple', '-'], 'NUR': ['tab:green', '-'], 'PAT': ['tab:orange', '-']},
               'sim': {'ADM': ['tab:blue', '--'], 'MED': ['tab:purple', '--'], 'NUR': ['tab:green', '--'], 'PAT': ['tab:orange', '--']}}
    for network in asympR0:
        for grp in asympR0[network]:
            ax1.plot(p, asympR0[network][grp], styles[network][grp][0], ls=styles[network][grp][1])
    
    for network in presympR0:
        for grp in presympR0[network]:
            ax2.plot(p, presympR0[network][grp], styles[network][grp][0], ls=styles[network][grp][1])
            print(network, grp, presympR0[network][grp])
    
    custom_lines = [Line2D([0], [0], color='tab:blue'), Line2D([0], [0], color='tab:purple'), Line2D([0], [0], color='tab:green'), Line2D([0], [0], color='tab:orange'),
                    Line2D([0], [0], color='black'), Line2D([0], [0], color='black', ls='--')]
    f.legend(custom_lines, ['ADM', 'MED', 'NUR', 'PAT', 'Emprirical', 'Simulated'], frameon=False, loc='upper left',  bbox_to_anchor=(1.0, 1.0))   
    ax1.set_title('Asymptomatic')
    ax2.set_title('Presymptomatic')
    f.supxlabel('p')
    f.supylabel(r'$R_0$')
    f.tight_layout()
    plt.savefig('pAgainstR.png', bbox_inches='tight')
    plt.show()

#plot_p_R0()

