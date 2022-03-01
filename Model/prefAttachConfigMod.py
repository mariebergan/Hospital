import random
from re import X
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.stats import poisson

groups = ['ADM', 'MED', 'NUR', 'PAT']
groupRange = {'ADM': [0, 8], 'MED': [8, 19], 'NUR': [19, 46], 'PAT': [46, 75]}

k_min = {'ADM': {'ADM': 4, 'MED': 0, 'NUR': 1, 'PAT': 0},
         'MED': {'ADM': 7, 'MED': 131, 'NUR': 23, 'PAT': 18},
         'NUR': {'ADM': 0, 'MED': 0, 'NUR': 58, 'PAT': 33},
         'PAT': {'ADM': 0, 'MED': 0, 'NUR': 0, 'PAT': 0}}

k_max = {'ADM': {'ADM': 258, 'MED': 269, 'NUR': 1096, 'PAT': 151},
         'MED': {'ADM': 174, 'MED': 1908, 'NUR': 472, 'PAT': 371},
         'NUR': {'ADM': 454, 'MED': 446, 'NUR': 3056, 'PAT': 852},
         'PAT': {'ADM': 112, 'MED': 143, 'NUR': 803, 'PAT': 117}}

stubs = {}
for ID in range(75):
    stubs[ID] = 0
degrees = {} # brukes til degree dist

for g1 in groups:
    degrees[g1] = {}
    for g2 in groups:
        degrees[g1][g2] = []
        for ID in range(groupRange[g1][0], groupRange[g1][1]):
            k = random.randint(k_min[g1][g2], k_max[g1][g2]) 
            stubs[ID] += k
            degrees[g1][g2].append(k)
        degrees[g1][g2].sort()

contacts = {}
for i in range(75):
    contacts[i] = {}
    for j in range(75):
        if i != j:
            contacts[i][j] = 1
        else:
            contacts[i][j] = 0

contactsArray = np.ones((75, 75), int)
np.fill_diagonal(contactsArray, 0)

for x in range(int((sum(list(stubs)))/2)):
    i = random.choice(list(stubs)) # velger random node som i
    stubs[i] -= 1
    p = []
    sumP = 0
    for ID in contacts[i]:
        sumP += contacts[i][ID]*stubs[ID]
    for ID in contacts[i]:
        pVal = (contacts[i][ID] * stubs[ID]) / sumP
        p.append(pVal)
    j = int(np.random.choice(a=list(stubs), size=1, p=p))

    stubs[i] -= 1
    stubs[j] -= 1
    contacts[i][j] += 1
    contacts[j][i] += 1
    contactsArray[i, j] += 1
    contactsArray[j, i] += 1

# Heatmap
config_hm = sns.heatmap(contactsArray, vmin = 1, vmax = 8)
config_hm.set_title('Preferential Attachement Config Model')
for x in [8, 19, 46]:
    config_hm.axhline(x, linewidth = 1, color = 'w')
    config_hm.axvline(x, linewidth = 1, color = 'w')

# Cumulative degree distributions
plt.style.use('seaborn')
f,((ax1, ax2, ax3, ax4), 
(ax5, ax6, ax7, ax8),
(ax9, ax10, ax11, ax12),
(ax13, ax14, ax15, ax16)) = plt.subplots(4, 4, figsize = (10, 7))
f.suptitle('Preferential Attachement Config model', fontsize = 'x-large') 
f.supylabel('Pk')
f.supxlabel('k')
axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16]

i = 0
for g1 in groups:
    for g2 in groups:
        x = degrees[g1][g2]
        y = np.arange(len(degrees[g1][g2]))/float(len(degrees[g1][g2]))
        axs[i].plot(x, 1-y)
        # axs[i].semilogy()
        # axs[i].semilogx()
        i += 1 

axs[12].set_xlabel('ADM')
axs[13].set_xlabel('MED')
axs[14].set_xlabel('NUR')
axs[15].set_xlabel('PAT')
axs[0].set_ylabel('ADM')
axs[4].set_ylabel('MED')
axs[8].set_ylabel('NUR')
axs[12].set_ylabel('PAT')
f.tight_layout()
plt.show()

