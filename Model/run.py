import matplotlib.pyplot as plt
from modelFuncs import *
from parameters import *
from empContacts import empDailyContactArrays
from configurationModel import configMod
from matplotlib.lines import Line2D

def runEmp():
    contactsArray = empDailyContactArrays
    attrs = initModel(contactsArray, baseP, nSeedNodes) 
    stateLog, absenceLog = timedRun_emp(contactsArray, attrs, baseP, startDay, runDays, testing=False, nContactArrays=4)
    return stateLog, absenceLog 

def runSim():
    contactsArray = configMod()[1]
    attrs = initModel(contactsArray, baseP, nSeedNodes) 
    stateLog, absenceLog = timedRun_sim(contactsArray, attrs, baseP, startDay, runDays, testing=False)
    return stateLog, absenceLog

def runEmp_testing():
    contactsArray = empDailyContactArrays
    attrs = initModel(contactsArray, baseP, nSeedNodes) 
    stateLog, absenceLog = timedRun_emp(contactsArray, attrs, baseP, startDay, runDays, testing=True, nContactArrays=4)
    return stateLog, absenceLog 
    
def runSim_testing():
    contactsArray = configMod()[1]
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
    plt.figure(figsize=(8, 5))
    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.plot(x, y3)
    plt.plot(x, y4)
    plt.xlabel('Day')
    plt.ylabel('N')
    plt.legend(['Susceptible', 'Exposed', 'Infected', 'Recovered'], frameon=False, loc='upper left',  bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig('empSEIR_p0.01.png', bbox_inches='tight')
    plt.show()

def plotAllStates(runModel, contactsArray):
    stateLog = runModel(contactsArray)[0]
    stateLog2 = rearrangeStateLog(stateLog)
    plt.figure(figsize=(8, 5))
    for state in stateList:
        x = list(range(runDays))
        y = stateLog2[state]
        plt.plot(x, y)
        plt.xlabel('Day')
        plt.ylabel('N')
    plt.legend(['Susceptible', 'Exposed', 'Asymptomatic', 'Presymptomatic', 'Symptomatic', 'Recovered', 'Hospitilized', 'ICU', 'Dead'],
                frameon=False, loc='upper left',  bbox_to_anchor=(1, 1))
    plt.tight_layout()
    plt.savefig('empStateLog_p0.01.png', bbox_inches='tight')
    plt.show()

def getInfRec(runModel, sims, ax1, ax2):
    avgInf = np.zeros(runDays, dtype = int)
    avgRec = np.zeros(runDays, dtype = int)
    for sim in range(sims):
        stateLog = runModel()[0]
        stateLog2 = rearrangeStateLog(stateLog)
        x = list(range(runDays))
        # inft
        y1 = mergeInfected(stateLog)
        ax1.plot(x, y1, 'r', alpha = 0.15)
        # rec 
        y2 = stateLog2['R']
        ax2.plot(x, y2, 'b', alpha = 0.15)
        for i in range(runDays):
            avgInf[i] += y1[i]
            avgRec[i] += y2[i]
    avgInf = avgInf/sims  
    avgRec = avgRec/sims    
    ax1.plot(x, avgInf, 'r')
    ax1.set_ylim([0, 50]) 
    ax2.plot(x, avgRec, 'b')
    ax2.set_ylim([0, 75])   
 

def infRecSubplot(runEmp, runSim, sims):
    f,((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=True, sharey='row', figsize = (8, 6))
    getInfRec(runEmp, sims, ax1, ax3)
    getInfRec(runSim, sims, ax2, ax4)
    ax1.set_title('Empirical')
    ax2.set_title('Simulated')
    f.supxlabel('Day')
    f.supylabel('N')
    custom_lines = [Line2D([0], [0], color='r'), Line2D([0], [0], color= 'b')]
    f.legend(custom_lines, ['Infected', 'Recovered'], frameon=False, loc='lower left',  bbox_to_anchor=(0.65, 0), ncol=2)   
    f.tight_layout()
    plt.savefig('infRec_p0.01_20sims_2.png', bbox_inches='tight')
    plt.show()

def absentHCW(sims):
    f, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(6, 6), sharey='row', sharex=True)
    avg1 = np.zeros(runDays, dtype = int)
    avg2 = np.zeros(runDays, dtype = int)
    avg3 = np.zeros(runDays, dtype = int)
    avg4 = np.zeros(runDays, dtype = int)
    avgInfs1 = np.zeros(runDays, dtype = int)
    avgInfs2 = np.zeros(runDays, dtype = int)
    avgInfs3 = np.zeros(runDays, dtype = int)
    avgInfs4 = np.zeros(runDays, dtype = int)

    for sim in range(sims):    
        print(sim)
        x = list(range(runDays)) 
        # Without testing, emp
        stateLog, y1 = runEmp()
        ax1.plot(x, y1, 'tab:blue', alpha=0.15)
        ax1.set_title('Empirical', fontsize=11)
        infs1 = mergeInfected(stateLog)
        for i in range(runDays):
            avg1[i] += y1[i]
            avgInfs1[i] += infs1[i]
        # Without testing, sim
        stateLog, y2 = runSim()
        ax2.plot(x, y2, 'tab:blue', alpha=0.15)
        ax2.set_title('Simulated', fontsize=11)
        infs2 = mergeInfected(stateLog)
        for i in range(runDays):
            avg2[i] += y2[i]
            avgInfs2[i] += infs2[i]
        # With testing, emp
        stateLog, y3 = runEmp_testing()
        ax3.plot(x, y3, 'tab:orange', alpha=0.15)
        infs3 = mergeInfected(stateLog)
        for i in range(runDays):
            avg3[i] += y3[i]
            avgInfs3[i] += infs3[i]
        # With testing, sim
        stateLog, y4 = runSim_testing()
        ax4.plot(x, y4, 'tab:orange', alpha=0.15)
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
    ax1.plot(x, avg1, 'tab:blue')
    ax2.plot(x, avg2, 'tab:blue')
    ax3.plot(x, avg3, 'tab:orange')
    ax4.plot(x, avg4, 'tab:orange')
    ax5.plot(x, avg1, 'tab:blue')
    ax6.plot(x, avg2, 'tab:blue')
    ax5.plot(x, avg3, 'tab:orange')
    ax6.plot(x, avg4, 'tab:orange')
    ax5.plot(x, avgInfs1, 'tab:blue', ls='--')
    ax6.plot(x, avgInfs2, 'tab:blue', ls='--')
    ax5.plot(x, avgInfs3, 'tab:orange', ls='--')
    ax6.plot(x, avgInfs4, 'tab:orange', ls='--') 

    f.supxlabel('            Day')
    f.supylabel('   N')
    mylabels = ['Without testing', 'With testing', 'Absent HCWs', 'Total infected']
    customLines = [Line2D([0], [0], color='tab:blue'), Line2D([0], [0], color= 'tab:orange'),
                   Line2D([0], [0], color='black'), Line2D([0], [0], color= 'black', ls='--')]
    f.legend(customLines, mylabels, frameon=False, loc='upper left',  bbox_to_anchor=(1.0, 0.96))
    f.tight_layout()
    plt.savefig('absentHCW_weekly_p0.01_20sims_NEW4.png', bbox_inches='tight')
    plt.show()

absentHCW(20)

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


