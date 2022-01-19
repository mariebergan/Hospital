import random
import numpy as np
from matplotlib import pyplot as plt

tab = {'ADM': {'ADM': [], 'MED': [], 'NUR': [], 'PAT': []},
       'MED': {'ADM': [], 'MED': [], 'NUR': [], 'PAT': []},
       'NUR': {'ADM': [], 'MED': [], 'NUR': [], 'PAT': []},
       'PAT': {'ADM': [], 'MED': [], 'NUR': [], 'PAT': []}}

groups = ['ADM', 'MED', 'NUR', 'PAT']


ADM_MED = [] #liste med node-IDene til ADM hvor hver ID er duplisert samme antall ganger som graden
for ID in range(1, 9):
    k = random.randint(0, 269)
    for i in range(k):
        ADM_MED.append(ID)
    random.shuffle(ADM_MED)

MED_ADM = []
for ID in range(9, 20):
    k = random.randint(0, 174)
    for i in range(k):
        MED_ADM.append(ID)
    random.shuffle(MED_ADM)

# connect nodes
links = []
for i in range(min(len(ADM_MED), len(MED_ADM))):
    links.append([ADM_MED[i], MED_ADM[i]])
AM = {}
MA = {}
count = 0
for link in links:
    i = links[count][0] # ADM ID
    j = links[count][1] # MED ID
    if i in AM:
        AM[i] += 1
    else:
        AM[i] = 1

    if j in MA:
        MA[j] += 1
    else:
        MA[j] = 1
    count += 1