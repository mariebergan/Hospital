from operator import ne
from re import A
import numpy as np
import seaborn as sns
from modelFuncs_seedNode import *
from InitializeParams import *
import matplotlib.pyplot as plt
from configurationModel import configMod
from empContactsArray import empContactsArray, empDailyContactArrays
from collections import Counter
from matplotlib.lines import Line2D
import scipy.stats as st

startDay = 0
runDays = 60

def runEmp(seedNode, seedState):
    attrs = initModel(empDailyContactArrays, baseP, seedNode, seedState)
    stateLog, infIDs, infBySeedNode = timedRun_emp(empDailyContactArrays, attrs, baseP, startDay, runDays, seedNode)
    return stateLog, infIDs, infBySeedNode

def runSim(seedNode, seedState):
    simDailyContactsArray = configMod()[1]
    attrs = initModel(simDailyContactsArray, baseP, seedNode, seedState)
    stateLog, infIDs, infBySeedNode = timedRun_sim(simDailyContactsArray, attrs, baseP, startDay, runDays, seedNode)
    return stateLog, infIDs, infBySeedNode

def runSim2(simDailyContactsArray, seedNode, seedState):
    attrs = initModel(simDailyContactsArray, baseP, seedNode, seedState)
    stateLog, infIDs, infBySeedNode = timedRun_sim(simDailyContactsArray, attrs, baseP, startDay, runDays, seedNode)
    return stateLog, infIDs, infBySeedNode

groups = ['ADM', 'MED', 'NUR', 'PAT']
groupRange = {'ADM': [0, 7], 'MED': [8, 18], 'NUR': [19, 45], 'PAT': [46, 74]}
seedStates = ['Ia', 'Ip']
networks = ['emp', 'sim']

def getSeedInfArray(sims):
    IaSeedInfArray = np.zeros((75, 75), dtype=int)
    IpSeedInfArray = np.zeros((75, 75), dtype=int)
    contactsArray = configMod()[1]
    for state in seedStates:
        for i in range(75): 
            print(i)
            for sim in range(sims):
                infIDs = runSim2(contactsArray, i, state)[1]
                for j in infIDs:
                    if state == 'Ia':
                        IaSeedInfArray[i][j] += 1
                    else:
                        IpSeedInfArray[i][j] += 1
    f = open('simIa_0.01.txt', 'w')
    for row in IaSeedInfArray:
        for x in row:
            f.write(str(x) + '\t')
        f.write('\n')
    f.close()
    f2 = open('simIp_0.01.txt', 'w')
    for row in IpSeedInfArray:
        for x in row:
            f2.write(str(x) + '\t')
        f2.write('\n')
    f2.close()
    print(IaSeedInfArray[0:10, 0:10])
    print(IpSeedInfArray[0:10, 0:10])

def genSeedNodeArray(file):
    seedNodeArray = np.zeros((75, 75), dtype=int)
    f = open(file)
    i = 0
    for line in f:
        splitLine = line.rstrip().split('\t')
        for j in range(75):
            x = int(splitLine[j])
            seedNodeArray[i][j] = x
        i += 1
    return seedNodeArray

def seedNodeHeatmap():
    f, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(6, 8), sharey=True, sharex=True)
    # Asymptomaitc             
    # a1 = genSeedNodeArray('empIa_0.01.txt')
    # a2 = genSeedNodeArray('simIa_0.01.txt')
    # a3 = genSeedNodeArray('empIa_0.005.txt')
    # a4 = genSeedNodeArray('simIa_0.005.txt')
    # a5 = genSeedNodeArray('empIa_0.001.txt')
    # a6 = genSeedNodeArray('simIa_0.001.txt')
    # Presymptomatic
    a1 = genSeedNodeArray('empIp_0.01.txt')
    a2 = genSeedNodeArray('simIp_0.01.txt')
    a3 = genSeedNodeArray('empIp_0.005.txt')
    a4 = genSeedNodeArray('simIp_0.005.txt')
    a5 = genSeedNodeArray('empIp_0.001.txt')
    a6 = genSeedNodeArray('simIp_0.001.txt')

    infArrays = [a1, a2, a3, a4, a5, a6]
    axs = [ax1, ax2, ax3, ax4, ax5, ax6]
    for x in range(6):
        hm = sns.heatmap(infArrays[x], ax=axs[x], vmin=0, vmax=100, xticklabels=False, yticklabels=False, cbar=False)
        for y in [8, 19, 46]:
            hm.axhline(y, linewidth = 1, color = 'w')
            hm.axvline(y, linewidth = 1, color = 'w')
            hm.axhline(y, linewidth = 1, color = 'w')
            hm.axvline(y, linewidth = 1, color = 'w')
    ax1.set_title('Empirical')
    ax2.set_title('Simulated')
    ax5.set_xlabel('ADM  MED         NUR                   PAT           ', fontsize=9)
    ax6.set_xlabel('ADM  MED         NUR                   PAT           ', fontsize=9)
    ax1.set_ylabel('          PAT               NUR       MED ADM', fontsize=9)
    ax3.set_ylabel('          PAT               NUR       MED ADM', fontsize=9)
    ax5.set_ylabel('          PAT               NUR       MED ADM', fontsize=9)
    f.supylabel('p = 0.001                                p = 0.005                                p = 0.01')
    f.tight_layout()
    plt.savefig('testSeedNode_presymp.png')
    plt.show()

seedNodeHeatmap()

def seedNodeHM(runEmp, empContacts, runSim, simContacts, sims):
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

#seedNodeHeatmap(runEmp, empDailyContactArrays, runSim, simDailyContactsArray, 2)

def getInfBySeedNode(runModel, contactsArray, sims):
    infBySeedNode = {}
    stateInf = {}
    for grp in groups:
        infBySeedNode[grp] = {'Ia' : [], 'Ip' : []}
        stateInf[grp] = {'Ia' : [], 'Ip' : []}
        for sim in range(sims):
            for state in seedStates:
                seedNode = random.randint(groupRange[grp][0], groupRange[grp][1])
                infs = runModel(contactsArray, seedNode, state)[2]
                stateInf[grp][state].append(infs)
        stateInf[grp]['Ia'].sort()
        stateInf[grp]['Ip'].sort()
        infBySeedNode[grp]['Ia'] = dict(Counter(stateInf[grp]['Ia']))
        infBySeedNode[grp]['Ip'] = dict(Counter(stateInf[grp]['Ip']))

    return infBySeedNode, stateInf

def aggregateAbove6(infBySeedNode):
    infBySeedNode_aggr = {}
    for grp in groups:
        infBySeedNode_aggr[grp] = {'Ia' : {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, '>6':0}, 'Ip' : {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, '>6':0}}
        for state in seedStates:
            for n in infBySeedNode[grp][state]:
                if n in range(7):
                    infBySeedNode_aggr[grp][state][n] += infBySeedNode[grp][state][n]
                else:
                    infBySeedNode_aggr[grp][state]['>6'] += infBySeedNode[grp][state][n]
    return infBySeedNode_aggr

def calculateR0(infBySeedNode, sims):
    R0 = {}
    for grp in groups:
        R0[grp] = {'Ia' : 0, 'Ip' : 0}
        for state in seedStates:
            R0[grp][state] = 0
            R = []
            for nInf in infBySeedNode[grp][state]:
                r = nInf * (infBySeedNode[grp][state][nInf]/sims)
                R.append(r)
            R0[grp][state] = round(sum(R), 2)
    return R0

def calculateR0confInt(stateInf):
    confInts = {}
    for grp in groups:
        confInts[grp] = {}
        for state in ['Ia', 'Ip']:
            confInt = st.norm.interval(alpha=0.95, loc=np.mean(stateInf[grp][state]), scale=st.sem(stateInf[grp][state]))
            confInts[grp][state] = list(np.around(confInt, 2))
    return confInts

def saveR0(runModel, contactsArray, sims, p):
    infBySeedNode, stateInf = getInfBySeedNode(runModel, contactsArray, sims)
    R0 = calculateR0(infBySeedNode, sims)
    f1 = open('simR0_file.txt', 'a')
    f1.write('p = ' + str(p) + '\t')
    for grp in groups:
        f1.write(str(R0[grp]['Ia']) + '\t')
    for grp in groups:
        f1.write(str(R0[grp]['Ip']) + '\t')
    f1.write('\n')
    f1.close()

    confInts = calculateR0confInt(stateInf)
    f2 = open('simConfInts_file.txt', 'a')
    f2.write('p = ' + str(p) + '\t')
    for grp in groups:
        f2.write(str(confInts[grp]['Ia'][0]) + '\t')
        f2.write(str(confInts[grp]['Ia'][1]) + '\t')
    for grp in groups:
        f2.write(str(confInts[grp]['Ip'][0]) + '\t')
        f2.write(str(confInts[grp]['Ip'][1]) + '\t')
    f2.write('\n')
    f2.close()

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
        for state in seedStates:
                for network in networks:
                    if network == 'emp':
                        x = list(infBySeedNode_aggr_emp[grp][state].values())
                        mylabels = list(infBySeedNode_aggr_emp[grp][state])
                        axs[i].pie(x)
                        axs[i].set_xlabel(r'$R_0$ = ' + str(R0_emp[grp][state]))
                    else:
                        x = list(infBySeedNode_aggr_sim[grp][state].values())
                        axs[i].pie(x)
                        axs[i].set_xlabel(r'$R_0$ = ' + str(R0_sim[grp][state]))

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

def getR0():
    R0 = {}
    for state in ['Ia', 'Ip']:
        R0[state] = {}
        for network in ['emp', 'sim']:
            R0[state][network] = {}
            for grp in groups:
                R0[state][network][grp] = []
    empR0 = open('empR0_file.txt')
    for line in empR0:
        splitLine = line.rstrip().split('\t')
        i = 1
        for grp in groups:
            R0['Ia']['emp'][grp].append(float(splitLine[i]))
            R0['Ip']['emp'][grp].append(float(splitLine[i+4]))
            i += 1
    empR0.close()
    simR0 = open('simR0_file.txt')
    for line in simR0:
        splitLine = line.rstrip().split('\t')
        i = 1
        for grp in groups:
            R0['Ia']['sim'][grp].append(float(splitLine[i]))
            R0['Ip']['sim'][grp].append(float(splitLine[i+4]))
            i += 1
    simR0.close()
    return R0

def getConfInts():
    confInts = {}
    for state in ['Ia', 'Ip']:
        confInts[state] = {}
        for network in ['emp', 'sim']:
            confInts[state][network] = {}
            for grp in groups:
                confInts[state][network][grp] = {}
                for bound in ['lower', 'upper']:
                    confInts[state][network][grp][bound] = []

    empConfInts = open('empConfInts_file.txt')
    for line in empConfInts:
        splitLine = line.rstrip().split('\t')
        i = 1
        for grp in groups:
            confInts['Ia']['emp'][grp]['lower'].append(float(splitLine[i]))
            confInts['Ia']['emp'][grp]['upper'].append(float(splitLine[i+1]))
            confInts['Ip']['emp'][grp]['lower'].append(float(splitLine[i+8]))
            confInts['Ip']['emp'][grp]['upper'].append(float(splitLine[i+9]))
            i += 2
    empConfInts.close()
    simConfInts = open('simConfInts_file.txt')
    for line in simConfInts:
        splitLine = line.rstrip().split('\t')
        i = 1
        for grp in groups:
            confInts['Ia']['sim'][grp]['lower'].append(float(splitLine[i]))
            confInts['Ia']['sim'][grp]['upper'].append(float(splitLine[i+1]))
            confInts['Ip']['sim'][grp]['lower'].append(float(splitLine[i+8]))
            confInts['Ip']['sim'][grp]['upper'].append(float(splitLine[i+9]))
            i += 2
    simConfInts.close()
    return confInts

styles = {'emp': {'ADM': ['tab:blue', '--'], 'MED': ['tab:purple', '--'], 'NUR': ['tab:green', '--'], 'PAT': ['tab:orange', '--']},
               'sim': {'ADM': ['tab:blue', '-'], 'MED': ['tab:purple', '-'], 'NUR': ['tab:green', '-'], 'PAT': ['tab:orange', '-']}}
customLines = [Line2D([0], [0], color='tab:blue'), Line2D([0], [0], color='tab:purple'), Line2D([0], [0], color='tab:green'), Line2D([0], [0], color='tab:orange'),
                    Line2D([0], [0], color='black', ls='--'), Line2D([0], [0], color='black')]

def plot_p_R0():
    p = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01]
    R0 = getR0()
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    axs = [ax1, ax2]
    i = 0
    for state in seedStates:
        for network in networks:
            for grp in groups:
                y = R0[state][network][grp]
                axs[i].plot(p, y, styles[network][grp][0], ls=styles[network][grp][1])
        i += 1
    
    f.legend(customLines, ['ADM', 'MED', 'NUR', 'PAT', 'Emprirical', 'Simulated'], frameon=False, loc='upper left',  bbox_to_anchor=(1.0, 1.0))
    ax1.set_title('Asymptomatic')
    ax2.set_title('Presymptomatic')
    f.supxlabel('p')
    f.supylabel(r'$R_0$')
    f.tight_layout()
    plt.savefig('pAgainstR.png', bbox_inches='tight')
    plt.show()

#plot_p_R0()

def plot_p_R0_confInts():
    p = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.01]
    R0 = getR0()
    confInts = getConfInts()
    f,((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8),
    (ax9, ax10, ax11, ax12), (ax13, ax14, ax15, ax16)) = plt.subplots(4, 4, figsize= (12, 7.5), sharex=True, sharey=True)
    axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16]
    i = 0
    for state in seedStates:
        for network in networks:
            j = 0
            for grp in groups:
                axs[i+j].plot(p, R0[state][network][grp], color=styles[network][grp][0], ls=styles[network][grp][1])
                ci_lower = confInts[state][network][grp]['lower']
                ci_upper = confInts[state][network][grp]['upper']
                axs[i+j].fill_between(p, ci_lower, ci_upper, alpha=0.3, color=styles[network][grp][0])
                j += 4
            i += 1  
    
    f.legend(customLines, ['ADM', 'MED', 'NUR', 'PAT', 'Emprirical', 'Simulated'], frameon=False, loc='lower left',  bbox_to_anchor=(0.25, -0.05), ncol=6)
    ax1.set_title('Empirical', fontsize=10)
    ax2.set_title('Simulated', fontsize=10)
    ax3.set_title('Empirical', fontsize=10)
    ax4.set_title('Simulated', fontsize=10)
    ax1.set_ylabel('ADM')
    ax5.set_ylabel('MED')
    ax9.set_ylabel('NUR')
    ax13.set_ylabel('PAT')
    f.suptitle('               Asymptomatic                                                                               Presymptomatic')
    f.supxlabel('p')
    f.supylabel(r'$R_0$')
    f.tight_layout()
    plt.savefig('p_R_withConfInts.png', bbox_inches='tight')
    plt.show()


