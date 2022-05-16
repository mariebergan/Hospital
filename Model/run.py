import matplotlib.pyplot as plt
from modelFuncs import *
from InitializeParams import *
from empContactsArray import empDailyContactArrays
from prefAttachConfigMod2 import simDailyContactsArray
from matplotlib.lines import Line2D

startDay = 0
runDays = 60
nSeedNodes = 1

def runEmp(contactsArray):
    attrs = initModel(contactsArray, baseP, nSeedNodes) 
    stateLog, absenceLog = timedRun_emp(contactsArray, attrs, baseP, startDay, runDays, testing=False)
    return stateLog, absenceLog 

# runEmp(empDailyContactArrays)
    
def runSim(contactsArray):
    attrs = initModel(contactsArray, baseP, nSeedNodes) 
    stateLog, absenceLog = timedRun_sim(contactsArray, attrs, baseP, startDay, runDays, testing=False)
    return stateLog, absenceLog

def runEmp_testing(contactsArray):
    attrs = initModel(contactsArray, baseP, nSeedNodes) 
    stateLog, absenceLog = timedRun_emp(contactsArray, attrs, baseP, startDay, runDays, testing=True)
    return stateLog, absenceLog 
    
def runSim_testing(contactsArray):
    attrs = initModel(contactsArray, baseP, nSeedNodes) 
    stateLog, absenceLog = timedRun_sim(contactsArray, attrs, baseP, startDay, runDays, testing=True)
    return stateLog, absenceLog

def rearrangeStateLog(stateLog):
    stateLog2 = {}
    for state in stateList:
        stateLog2[state] = []
    for i in range(runDays):
        for state in stateList:
            stateLog2[state].append(stateLog[i][state])
    return stateLog2

def mergeInfected(stateLog):
    infectedStates = ['Ia', 'Ip', 'Is', 'H', 'ICU']
    infected = [0]*runDays
    for day in range(runDays):
        for state in infectedStates:
            infected[day] += stateLog[day][state]
    return infected

def plotSEIR(runModel, contactsArray):
    stateLog = runModel(contactsArray)[0]
    stateLog2 = rearrangeStateLog(stateLog)
    x = list(range(runDays))
    y1 = stateLog2['S']
    y2 = stateLog2['E']
    y3 = mergeInfected(stateLog)
    y4 = stateLog2['R']
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.plot(x, y3)
    plt.plot(x, y4)
    plt.xlabel('Day')
    plt.ylabel('N')
    plt.legend(['Susceptible', 'Exposed', 'Infected', 'Recovered'], loc='center right')
    plt.show()

#plotSEIR(runEmp_testing, empDailyContactArrays)

def plotAllStates(runModel, contactsArray):
    stateLog = runModel(contactsArray)[0]
    stateLog2 = rearrangeStateLog(stateLog)
    for state in stateList:
        x = list(range(runDays))
        y = stateLog2[state]
        plt.plot(x, y)
        plt.xlabel('Day')
        plt.ylabel('N')
        plt.legend(['Susceptible', 'Exposed', 'Asymptomatic', 'Presymptomatic', 'Symptomatic', 'Recovered', 'Hospitilized', 'ICU', 'Dead'],
                loc='center right')
    plt.show()

#plotAllStates(runSim, simDailyContactsArray)
#plotAllStates(runEmp, empDailyContactArrays)

def plotInfected(runModel, contactsArray, sims, ax):
    avgInf = np.zeros(runDays, dtype = int)
    for sim in range(sims):
        stateLog = runModel(contactsArray)[0]
        x = list(range(runDays))
        y = mergeInfected(stateLog)
        ax.plot(x, y, 'r', alpha = 0.15)
        for i in range(runDays):
            avgInf[i] += y[i]
    avgInf = avgInf/sims     
    ax.plot(x, avgInf, 'r')
    ax.set_ylim([0, 40])    

def plotRecovered(runModel, contactsArray, sims, ax):
    avgRec = np.zeros(runDays, dtype = int)
    for sim in range(sims):
        stateLog = runModel(contactsArray)[0]
        stateLog2 = rearrangeStateLog(stateLog)
        x = list(range(runDays))
        y = stateLog2['R']
        ax.plot(x, y, 'b', alpha = 0.15)
        for i in range(runDays):
            avgRec[i] += y[i]
    avgRec = avgRec/sims 
    ax.plot(x, avgRec, 'b')
    ax.set_ylim([0, 40])    

def infRecSubplot(runEmp, runSim, empDailyContactArrays, simContactsArray, sims):
    f,((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=True, sharey=True, figsize = (8, 6))
    plotInfected(runEmp, empDailyContactArrays, sims, ax1)
    plotInfected(runSim, simContactsArray, sims, ax2)
    plotRecovered(runEmp, empDailyContactArrays, sims, ax3)
    plotRecovered(runSim, simContactsArray, sims, ax4)
    ax1.set_title('Empirical')
    ax2.set_title('Simulated')
    f.supxlabel('Day')
    f.supylabel('N')
    custom_lines = [Line2D([0], [0], color='r'), Line2D([0], [0], color= 'b')]
    f.legend(custom_lines, ['Infected', 'Recovered'], frameon=False, loc='upper left',  bbox_to_anchor=(1.0, 0.95))   
    f.tight_layout()
    plt.savefig('infRec_p0.001.png', bbox_inches='tight')
    plt.show()

#infRecSubplot(runEmp, runSim, empDailyContactArrays, simDailyContactsArray, 20)   

def absentHCW(empContacts, simContacts, sims):
    f, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(6, 6), sharey=True, sharex=True)
    
    avg1 = np.zeros(runDays, dtype = int)
    avg2 = np.zeros(runDays, dtype = int)
    avg3 = np.zeros(runDays, dtype = int)
    avg4 = np.zeros(runDays, dtype = int)

    avgInfs1 = np.zeros(runDays, dtype = int)
    avgInfs2 = np.zeros(runDays, dtype = int)
    avgInfs3 = np.zeros(runDays, dtype = int)
    avgInfs4 = np.zeros(runDays, dtype = int)

    for sim in range(sims):    
        x = list(range(runDays)) 
        # Without testing, emp
        stateLog, y1 = runEmp(empContacts)
        ax1.plot(x, y1, 'tab:blue', alpha=0.3)
        ax1.set_title('Empirical', fontsize=11)

        infs1 = mergeInfected(stateLog)
        for i in range(runDays):
            avg1[i] += y1[i]
            avgInfs1[i] += infs1[i]

        # Without testing, sim
        stateLog, y2 = runSim(simContacts)
        ax2.plot(x, y2, 'tab:blue', alpha=0.3)
        ax2.set_title('Simulated', fontsize=11)
        infs2 = mergeInfected(stateLog)
        for i in range(runDays):
            avg2[i] += y2[i]
            avgInfs2[i] += infs2[i]
        # With testing, emp
        stateLog, y3 = runEmp_testing(empContacts)
        ax3.plot(x, y3, 'tab:orange', alpha=0.3)
        infs3 = mergeInfected(stateLog)
        for i in range(runDays):
            avg3[i] += y3[i]
            avgInfs3[i] += infs3[i]
        # With testing, sim
        stateLog, y4 = runSim_testing(simContacts)
        ax4.plot(x, y4, 'tab:orange', alpha=0.3)
        infs4 = mergeInfected(stateLog)
        for i in range(runDays):
            avg4[i] += y4[i]
            avgInfs4[i] += infs4[i]
    
    avg1 = avg1/sims
    avg2 = avg2/sims
    avg3 = avg3/sims
    avg4 = avg4/sims
    avgInfs1 = avgInfs1/sims
    avgInfs2 = avgInfs2/sims
    avgInfs3 = avgInfs3/sims
    avgInfs4 = avgInfs4/sims
    
    ax5.plot(x, avg1, 'tab:blue')
    ax6.plot(x, avg2, 'tab:blue')
    ax5.plot(x, avg3, 'tab:orange')
    ax6.plot(x, avg4, 'tab:orange')

    ax5.plot(x, avgInfs1, 'tab:blue', ls='--')
    ax6.plot(x, avgInfs2, 'tab:blue', ls='--')
    ax5.plot(x, avgInfs3, 'tab:orange', ls='--')
    ax6.plot(x, avgInfs4, 'tab:orange', ls='--')

    f.suptitle('Absent Health Care Workers, p = 0.005')
    f.supxlabel('Day')
    f.supylabel('N')
    mylabels = ['Without testing', 'With testing', 'Absent HCWs', 'Total infected']
    customLines = [Line2D([0], [0], color='tab:blue'), Line2D([0], [0], color= 'tab:orange'),
                   Line2D([0], [0], color='black'), Line2D([0], [0], color= 'black', ls='--')]
    f.legend(customLines, mylabels, frameon=False, loc='upper left',  bbox_to_anchor=(1.0, 1.0))
    f.tight_layout()
    plt.savefig('absentHCW_10sims_p0.005.png', bbox_inches='tight')
    plt.show()

absentHCW(empDailyContactArrays, simDailyContactsArray, 10)

def absentHCW_old(empContacts, simContacts):
    f, ((ax1, ax2)) = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

    x = list(range(runDays))
    # Empirical
    y1 = runEmp(empContacts)[1]
    ax1.plot(x, y1)
    y2 = runEmp_testing(empContacts)[1]
    ax1.plot(x, y2)
    ax1.set_title('Empirical', fontsize=11)
    ax1.set_ylim([0, 20])
    # Simulated
    y3 = runSim(simContacts)[1]
    ax2.plot(x, y3)
    y4 = runSim_testing(simContacts)[1]
    ax2.plot(x, y4)
    ax2.set_title('Simulated', fontsize=11)
    ax2.set_ylim([0, 20])
       
    f.suptitle('Absent Health Care Workers, p = 0.001')
    f.supxlabel('Day')
    f.supylabel('N')
    mylabels = ['Without testing', 'With testing']
    f.legend(mylabels, frameon=False, loc='upper left',  bbox_to_anchor=(1.0, 1.0))
    f.tight_layout()
    plt.savefig('absentHCW_p0.001.png', bbox_inches='tight')
    plt.show()

#absentHCW_old(empDailyContactArrays, simDailyContactsArray)

