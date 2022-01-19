import random
import numpy as np
from matplotlib import pyplot as plt

### ADM ###
ADM_1 = []
ADM_2 = []
for ID in range(1, 9):
    k = random.randint(0, 258)
    for i in range(k):
        ADM_1.append(ID)
        ADM_2.append(ID)
    random.shuffle(ADM_1)
    random.shuffle(ADM_2)

# connect nodes
links = []
for i in range(len(ADM_1)):
    links.append([ADM_1[i], ADM_2[i]])

A = {}
count = 0
for link in links:
    i = links[count][0] # source node ID
    j = links[count][1] # targe node ID
    if i in A:
        A[i] += 1
    else:
        A[i] = 1
    count += 1
A = list(A.values())

### MED ###
MED_1 = []
MED_2 = []
for ID in range(9, 20):
    k = random.randint(0, 1908)
    for i in range(k):
        MED_1.append(ID)
        MED_2.append(ID)
    random.shuffle(MED_1)
    random.shuffle(MED_2)

links = []
for i in range(len(MED_1)):
    links.append([MED_1[i], MED_2[i]])

M = {}
count = 0
for link in links:
    i = links[count][0] 
    j = links[count][1] 
    if i in M:
        M[i] += 1
    else:
        M[i] = 1
    count += 1
M = list(M.values())

### NUR ###
NUR_1 = []
NUR_2 = []
for ID in range(20, 47):
    k = random.randint(0, 3056)
    for i in range(k):
        NUR_1.append(ID)
        NUR_2.append(ID)
    random.shuffle(NUR_1)
    random.shuffle(NUR_2)

for i in range(len(NUR_1)):
    links.append([NUR_1[i], NUR_2[i]])

N = {}
count = 0
for link in links:
    i = links[count][0] 
    j = links[count][1] 
    if i in N:
        N[i] += 1
    else:
        N[i] = 1
    count += 1
N = list(N.values())

### PAT ###
PAT_1 = []
PAT_2 = []
for ID in range(47, 76):
    k = random.randint(0, 117)
    for i in range(k):
        PAT_1.append(ID)
        PAT_2.append(ID)
    random.shuffle(PAT_1)
    random.shuffle(PAT_2)

for i in range(len(PAT_1)):
    links.append([PAT_1[i], PAT_2[i]])

P = {}
count = 0
for link in links:
    i = links[count][0] 
    j = links[count][1] 
    if i in P:
        P[i] += 1
    else:
        P[i] = 1
    count += 1
P = list(P.values())

