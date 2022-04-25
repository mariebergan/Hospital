import numpy as np
import seaborn as sns
from modelFuncs_seedNode import *
from InitializeParams import *
import matplotlib.pyplot as plt
from prefAttachConfigMod2 import dailyContactsArray

seedInfArr = np.zeros((75, 75), dtype=int)
for i in range(75):
    print(i)
    for sim in range(100):
        attrs = initModel(dailyContactsArray, baseP, i)
        stateLog, infLog, ageLog, day, infIDs = timedRun(dailyContactsArray, attrs, baseP, 0, 60)

        for j in infIDs:
            seedInfArr[i][j] += 1

hm = sns.heatmap(seedInfArr)
hm.set_title('Configuration Model')
plt.show()
