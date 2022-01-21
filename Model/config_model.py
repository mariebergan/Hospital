import random
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

groups = ['ADM', 'MED', 'NUR', 'PAT']
tab = {}

for g1 in groups:
    tab[g1] = {}
    for g2 in groups:
        tab[g1][g2] = []

k_min = {'ADM': {'ADM': 4, 'MED': 0, 'NUR': 1, 'PAT': 0},
         'MED': {'ADM': 7, 'MED': 131, 'NUR': 23, 'PAT': 18},
         'NUR': {'ADM': 0, 'MED': 0, 'NUR': 58, 'PAT': 33},
         'PAT': {'ADM': 0, 'MED': 0, 'NUR': 0, 'PAT': 0}}

k_max = {'ADM': {'ADM': 258, 'MED': 269, 'NUR': 1096, 'PAT': 151},
         'MED': {'ADM': 174, 'MED': 1908, 'NUR': 472, 'PAT': 371},
         'NUR': {'ADM': 454, 'MED': 446, 'NUR': 3056, 'PAT': 852},
         'PAT': {'ADM': 112, 'MED': 143, 'NUR': 803, 'PAT': 117}}


for g1 in groups:
    for g2 in groups:
        
        if g1 == 'ADM':
            for ID in range(1, 9):
                k = random.randint(k_min[g1][g2], k_max[g1][g2])
                for i in range(k):
                    tab[g1][g2].append(ID)
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

contacts = np.zeros((76, 76), dtype = int)
# diagonal
for g1 in groups:
    for x in range(0, (len(tab[g1][g2])-1), 2): 
        i = tab[g1][g1][x] # source ID
        j = tab[g1][g1][x+1] # target ID

        if contacts[i, j] == 0:
            contacts[i, j] = 1
            contacts[j, i] = 1

        else:
            contacts[i, j] += 1
            contacts[j, i] += 1

# non-diagonal
for g1 in groups:
    for g2 in groups:
        if g1 != g2:
            for x in range(min(len(tab[g1][g2]), len(tab[g2][g1]))): 
                i = tab[g1][g2][x] # source ID
                j = tab[g2][g1][x] # target ID

                if contacts[i, j] == 0:
                    contacts[i, j] = 1
                    contacts[j, i] = 1

                else:
                    contacts[i, j] += 1
                    contacts[j, i] += 1

contacts = contacts[1:76, 1:76] # IDene starter på 1

# heatmap
config_hm = sns.heatmap(contacts)
config_hm.set_title('Configuration model')
for x in [8, 19, 46]:
    config_hm.axhline(x, linewidth = 0.5, color = 'w')
    config_hm.axvline(x, linewidth = 0.5, color = 'w')

# cumulative degree distributions

degrees = {}

for g1 in groups:
    degrees[g1] = {}
    for g2 in groups:
        degrees[g1][g2] = []

        for ID in tab[g1][g2]:
            degrees[g1][g2].append()