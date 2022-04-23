import numpy as np
import seaborn as sns
from modelFuncs import *
from InitializeParams import *
import matplotlib.pyplot as plt
from empContactsArr import empContactArrays

seedInfArr = np.zeros((75, 75), dtype=int)
for i in range(75):
    for sim in range(100):
        attrs = initModel(empContactArrays, baseP, i)
        stateLog, infLog, ageLog, day, infIDs = timedRun(empContactArrays, attrs, baseP, 0, 60)

        for j in infIDs:
            seedInfArr[i][j] += 1

sns.heatmap(seedInfArr)
plt.show()



      

    


