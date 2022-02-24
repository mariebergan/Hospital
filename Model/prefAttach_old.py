import random
import numpy as np
from matplotlib import pyplot as plt

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


for g1 in groups:
    tab[g1] = {}
    for g2 in groups:
        tab[g1][g2] = []

        if g1 == 'ADM':
            for ID in range(1, 9):
                k = random.randint(k_min[g1][g2], k_max[g1][g2]) 
                for x in range(k):
                    tab[g1][g2].append(ID) # legger til den aktuelle IDen samme antall ganger som graden (k)
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


contacts = np.ones((76, 76), int)
np.fill_diagonal(contacts, 0)

# Diagonal
for g1 in groups:
    stubs = tab[g1][g1]
    for x in range(int((len(stubs))/2)):
        print(x)
        i = stubs[0] 
        stubs.remove(i)

        edgeWeights = []    
        for j in stubs: # denne loopen som tar tid, looper en gang for mye?
            edgeWeights.append(contacts[i, j])
            p = [Wij/sum(edgeWeights) for Wij in edgeWeights]  
        j = np.random.choice(a=stubs, size=1, p=p)
        stubs.remove(j)
        contacts[i, j] += 1
        contacts[j, i] += 1

        # stubs_2 = []
        # for j in stubs: 
        #     Wij = contacts[i, j] 
        #     stubs_2.extend(j for y in range(Wij)) # ny versjon av stubs hvor j er duplisert med vekten
        # index = random.randint(0, len(stubs_2)-1)
        # j = stubs_2[index]
         
# Non-diagonal
# for g1 in groups:
#     for g2 in groups:
#         sourcestubs = tab[g1][g2]
#         targetstubs = tab[g2][g1]
#         if g1 != g2:
#             for x in range(min(len(tab[g1][g2]), len(tab[g2][g1]))): 
#                 i = sourcestubs[0]
#                 sourcestubs.remove(i)

#                 for j in targetstubs:
#                     Wij = contacts[i, j] 
#                     targetstubs_2 = targetstubs.extend(j for x in range(Wij))
                
#                 random.shuffle(targetstubs_2)
#                 j = targetstubs_2[0] 
#                 contacts[i, j] += 1
#                 contacts[j, i] += 1
#                 targetstubs.remove(j) 

