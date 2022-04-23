from modelFuncs import *
from InitializeParams import *
import matplotlib.pyplot as plt
from empContactsArr import empContactArrays


startDay = 0
runDays = 60
attrs = initModel(empContactArrays, baseP, 1) # n = # seed nodes

stateLog, infLog, ageLog, day, infIDs = timedRun(empContactArrays, attrs, baseP, 0, 60)

stateLog2 = {}
for state in stateList:
    stateLog2[state] = []

for i in range(runDays):
    for state in stateList:
        stateLog2[state].append(stateLog[i][state])
        
# plot stateLog
for state in stateList:
    x = list(range(runDays))
    y = stateLog2[state]
    plt.plot(x, y)
    plt.xlabel('Day')
    plt.ylabel('N')
    plt.title('Empirical')
    plt.legend(['Susceptible', 'Exposed', 'Asymptomatic', 'Presymptomatic', 'Symptomatic', 'Recovered', 'Hospitilized', 'ICU', 'Dead'],
            loc='center right')
plt.show()



