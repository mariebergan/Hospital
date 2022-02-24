import random
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from collections import Counter

groups = ['ADM', 'MED', 'NUR', 'PAT']
tab = {}

k_min = {'ADM': {'ADM': 4, 'MED': 0, 'NUR': 1, 'PAT': 0},
         'MED': {'ADM': 7, 'MED': 131, 'NUR': 23, 'PAT': 18},
         'NUR': {'ADM': 0, 'MED': 0, 'NUR': 58, 'PAT': 33},
         'PAT': {'ADM': 0, 'MED': 0, 'NUR': 0, 'PAT': 0}}

k_max = {'ADM': {'ADM': 258, 'MED': 269, 'NUR': 1096, 'PAT': 151},
         'MED': {'ADM': 174, 'MED': 1908, 'NUR': 472, 'PAT': 371},
         'NUR': {'ADM': 454, 'MED': 446, 'NUR': 3056, 'PAT': 852},
         'PAT': {'ADM': 112, 'MED': 143, 'NUR': 803, 'PAT': 117}}

k_sum = {'ADM': {'ADM': 558, 'MED': 459, 'NUR': 2596, 'PAT': 441},
         'MED': {'ADM': 459, 'MED': 11320, 'NUR': 1769, 'PAT': 1471},
         'NUR': {'ADM': 2596, 'MED': 1769, 'NUR': 25390, 'PAT': 6835},
         'PAT': {'ADM': 441, 'MED': 1471, 'NUR': 6845, 'PAT': 418}}

for g1 in groups:
    tab[g1] = {}
    for g2 in groups:
        tab[g1][g2] = []
        
        if g1 == 'ADM':
            for ID in range(1, 9):
                k = random.randint(k_min[g1][g2], k_max[g1][g2]) # summen av k for alle nodene skal bli 558, hvordan begrense dette?
                for i in range(k):
                    tab[g1][g2].append(ID) ### lengden på denne listen, som tilsvarer antall kontakter innad i ADM (ADM_ADM), må være på k_sum['ADM']['ADM'] = 558
                random.shuffle(tab[g1][g2])

        elif g1 == 'MED':    
            for ID in range(9, 20):
                k = random.randint(k_min[g1][g2], k_max[g1][g2])
                for i in range(k):
                    tab[g1][g2].append(ID)
                random.shuffle(tab[g1][g2])
        
        elif g1 == 'NUR':
            for ID in range(20, 47):
                k = random.randint(k_min[g1][g2], k_max[g1][g2])
                for i in range(k):
                    tab[g1][g2].append(ID)
                random.shuffle(tab[g1][g2])
        
        elif g1 == 'PAT':
            for ID in range(47, 76):
                k = random.randint(k_min[g1][g2], k_max[g1][g2])
                for i in range(k):
                    tab[g1][g2].append(ID)
                random.shuffle(tab[g1][g2])

print(sorted(tab['ADM']['ADM']))
contacts = np.zeros((76, 76), dtype = int)

# diagonal
for g1 in groups:
    for x in range(0, (len(tab[g1][g2])-1), 2): 
        i = tab[g1][g1][x] # source ID
        j = tab[g1][g1][x+1] # target ID

        if (contacts[i, j]) == 0 and (i != j):
            contacts[i, j] = 1
            contacts[j, i] = 1

        elif (i!=j):
            contacts[i, j] += 1
            contacts[j, i] += 1

# non-diagonal
for g1 in groups:
    for g2 in groups:
        if g1 != g2:
            for x in range(min(len(tab[g1][g2]), len(tab[g2][g1]))): 
                i = tab[g1][g2][x] 
                j = tab[g2][g1][x] 

                if (contacts[i, j]) == 0 and (i != j):
                    contacts[i, j] = 1
                    contacts[j, i] = 1

                elif (i!=j):
                    contacts[i, j] += 1
                    contacts[j, i] += 1

contacts = contacts[1:76, 1:76] # IDene starter på 1
contacts = contacts + 1
contacts = np.log(contacts)

# Heatmap
config_hm = sns.heatmap(contacts, vmin = 1, vmax = 8)
config_hm.set_title('Configuration Model')
for x in [8, 19, 46]:
    config_hm.axhline(x, linewidth = 0.5, color = 'w')
    config_hm.axvline(x, linewidth = 0.5, color = 'w')


# Cumulative degree distributions        
degrees = {}
for g1 in groups:
    degrees[g1] = {}
    for g2 in groups:
        occurences = Counter(tab[g1][g2])
        degrees[g1][g2] = list(occurences.values())

        # add nodes with k = 0
        if g1 == 'ADM' and len(degrees['ADM'][g2]) < 8:
            degrees['ADM'][g2].extend([0 for i in range(8-len(degrees['ADM'][g2]))])
        
        if g1 == 'MED' and len(degrees['MED'][g2]) < 11:
            degrees['MED'][g2].extend([0 for i in range(11-len(degrees['MED'][g2]))])
        
        if g1 == 'NUR' and len(degrees['NUR'][g2]) < 27:
            degrees['NUR'][g2].extend([0 for i in range(27-len(degrees['NUR'][g2]))])
        
        if g1 == 'PAT' and len(degrees['PAT'][g2]) < 29:
            degrees['PAT'][g2].extend([0 for i in range(29-len(degrees['PAT'][g2]))])

        #degrees[g1][g2] = sorted(degrees[g1][g2])

        # k_sum = sum(degrees[g1][g2])
        # print(k_sum)

plt.style.use('seaborn')

f,((ax1, ax2, ax3, ax4), 
(ax5, ax6, ax7, ax8),
(ax9, ax10, ax11, ax12),
(ax13, ax14, ax15, ax16)) = plt.subplots(4, 4, figsize = (10, 7))

f.suptitle('Cumulative degree distributions - Configuration model', fontsize = 'x-large') 
f.supylabel('Pk')
f.supxlabel('k')

axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16]

i = 0
for g1 in groups:
    for g2 in groups:
        x = np.cumsum(degrees[g1][g2])
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





