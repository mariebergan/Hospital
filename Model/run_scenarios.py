from tkinter import N
import matplotlib.pyplot as plt
from modelFuncs import *
from InitializeParams import *
from empContactsArray import empDailyContactArrays
from configurationModel import *
from matplotlib.lines import Line2D


startDay = 0
runDays = 60
nSeedNodes = 1

def runEmp():
    contactsArray = empDailyContactArrays
    attrs = initModel(contactsArray, baseP, nSeedNodes)
    stateLog, absenceLog = timedRun_emp(contactsArray, attrs, baseP, startDay, runDays, testing=False, nContactArrays=4)
    return stateLog, absenceLog

# Scenario 1
def runSim1():
    contactsArray = configMod()[1]
    attrs = initModel(contactsArray, baseP, nSeedNodes)
    stateLog, absenceLog = timedRun_sim(contactsArray, attrs, baseP, startDay, runDays, testing=False)
    return stateLog, absenceLog

# Scanerio 2
def runSim2():
    n = 4
    contactArrays = []
    for i in range(n):
        print('scenario2', 'array=', i)
        dailyContacts = configMod()[1]
        contactArrays.append(dailyContacts)
    attrs = initModel(contactArrays, baseP, nSeedNodes)
    stateLog, absenceLog = timedRun_emp(contactArrays, attrs, baseP, startDay, runDays, testing=False, nContactArrays=n)
    return stateLog, absenceLog

# Scenario 3
def runSim3():
    n = 60
    contactArrays = []
    for i in range(n):
        print('scenario3', 'array=', i)
        dailyContacts = configMod()[1]
        contactArrays.append(dailyContacts)
    attrs = initModel(contactArrays, baseP, nSeedNodes)
    stateLog, absenceLog = timedRun_emp(contactArrays, attrs, baseP, startDay, runDays, testing=False, nContactArrays=n)
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

def getInfRec(runModel, sims, infAx, recAx):
    avgInf = np.zeros(runDays, dtype = int)
    avgRec = np.zeros(runDays, dtype = int)
    for sim in range(sims):
        print('sim=', sim)
        # inf
        stateLog, absenceLog = runModel()
        x1 = list(range(runDays))
        y1 = mergeInfected(stateLog)
        infAx.plot(x1, y1, 'r', alpha = 0.15)
        # rec
        x2 = list(range(runDays))
        stateLog2 = rearrangeStateLog(stateLog)
        y2 = stateLog2['R']
        recAx.plot(x2, y2, 'b', alpha = 0.15)
        for i in range(runDays):
            avgInf[i] += y1[i]
            avgRec[i] += y2[i]
    avgInf = avgInf/sims
    infAx.plot(x1, avgInf, 'r')
    infAx.set_ylim([0, 50])
    avgRec = avgRec/sims
    recAx.plot(x2, avgRec, 'b')
    recAx.set_ylim([0, 75])

def infRecSubplot(sims):
    f,((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = plt.subplots(2, 4, sharex=True, sharey='row', figsize = (10, 6))
    getInfRec(runEmp, sims, ax1, ax5)
    print('emp')
    getInfRec(runSim1, sims, ax2, ax6)
    print('sim1')
    getInfRec(runSim2, sims, ax3, ax7)
    print('sim2')
    getInfRec(runSim3, sims, ax4, ax8)
    print('sim3')
    ax1.set_title('Empirical')
    ax2.set_title('Simulated 1')
    ax3.set_title('Simulated 2')
    ax4.set_title('Simulated 3')
    f.supxlabel('Day')
    f.supylabel('N')
    custom_lines = [Line2D([0], [0], color='r'), Line2D([0], [0], color= 'b')]
    f.legend(custom_lines, ['Infected', 'Recovered'], frameon=False, loc='lower left',  bbox_to_anchor=(0.75, 0), ncol=2)   
    f.tight_layout()
    plt.savefig('infRec_scenarios_p0.005.png', bbox_inches='tight')
    plt.show()

#infRecSubplot(20)

## emp daily
def runEmpDaily(contactsArray):
    attrs = initModel(contactsArray, baseP, nSeedNodes)
    stateLog, absenceLog = timedRun_sim(contactsArray, attrs, baseP, startDay, runDays, testing=False)
    return stateLog, absenceLog

def getInfRecEmpDaily(runModel, contactsArray, sims, infAx, recAx):
    avgInf = np.zeros(runDays, dtype = int)
    avgRec = np.zeros(runDays, dtype = int)
    for sim in range(sims):
        print('sim=', sim)
        # inf
        stateLog, absenceLog = runModel(contactsArray)
        x1 = list(range(runDays))
        y1 = mergeInfected(stateLog)
        infAx.plot(x1, y1, 'r', alpha = 0.15)
        # rec
        x2 = list(range(runDays))
        stateLog2 = rearrangeStateLog(stateLog)
        y2 = stateLog2['R']
        recAx.plot(x2, y2, 'b', alpha = 0.15)
        for i in range(runDays):
            avgInf[i] += y1[i]
            avgRec[i] += y2[i]
    avgInf = avgInf/sims
    infAx.plot(x1, avgInf, 'r')
    avgRec = avgRec/sims
    recAx.plot(x2, avgRec, 'b')
    infAx.set_ylim([0, 40])
    recAx.set_ylim([0, 75])


def infRecSubplotEmpDaily(sims):
    f,((ax1, ax2, ax3, ax4, ax5), (ax6, ax7, ax8, ax9, ax10)) = plt.subplots(2, 5, sharex=True, sharey='row', figsize = (11, 6))
    getInfRec(runEmp, sims, ax1, ax6)
    getInfRecEmpDaily(runEmpDaily, empDailyContactArrays[0], sims, ax2, ax7)
    getInfRecEmpDaily(runEmpDaily, empDailyContactArrays[1], sims, ax3, ax8)
    getInfRecEmpDaily(runEmpDaily, empDailyContactArrays[2], sims, ax4, ax9)
    getInfRecEmpDaily(runEmpDaily, empDailyContactArrays[3], sims, ax5, ax10)
    

    ax1.set_title('Total')
    ax2.set_title('Day 1')
    ax3.set_title('Day 2')
    ax4.set_title('Day 3')
    ax5.set_title('Day 4')
    f.supxlabel('Day')
    f.supylabel('N')
    custom_lines = [Line2D([0], [0], color='r'), Line2D([0], [0], color= 'b')]
    f.legend(custom_lines, ['Infected', 'Recovered'], frameon=False, loc='lower left',  bbox_to_anchor=(0.75, 0), ncol=2)   
    f.tight_layout()
    plt.savefig('infRec_empDaily_p0.005_20sims.png', bbox_inches='tight')
    plt.show()

infRecSubplotEmpDaily(20)