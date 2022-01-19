import random
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

### ADM ###
ADM_1 = []
ADM_2 = []
for ID in range(1, 9):
    k = random.randint(4, 258)
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
    k = random.randint(131, 1908)
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
    k = random.randint(58, 3056)
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



### ADM + MED ###
ADM_MED = [] #liste med node-IDene til ADM hvor hver ID er duplisert samme antall ganger som graden
for ID in range(1, 9):
    k = random.randint(0, 269)
    for i in range(k):
        ADM_MED.append(ID)
    random.shuffle(ADM_MED)

MED_ADM = []
for ID in range(9, 20):
    k = random.randint(7, 174)
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

AM = list(AM.values())
MA = list(MA.values())

### ADM + NUR ###
ADM_NUR = [] 
for ID in range(1, 9):
    k = random.randint(1, 1096)
    for i in range(k):
        ADM_NUR.append(ID)
    random.shuffle(ADM_NUR)

NUR_ADM = []
for ID in range(20, 47):
    k = random.randint(0, 454)
    for i in range(k):
        NUR_ADM.append(ID)
    random.shuffle(NUR_ADM)

links = []
for i in range(min(len(ADM_NUR), len(NUR_ADM))):
    links.append([ADM_NUR[i], NUR_ADM[i]])

AN = {}
NA = {}
count = 0
for link in links:
    i = links[count][0] # ADN ID
    j = links[count][1] # NUR ID
    if i in AN:
        AN[i] += 1
    else:
        AN[i] = 1

    if j in NA:
        NA[j] += 1
    else:
        NA[j] = 1
    count += 1
AN = list(AN.values())
NA = list(NA.values())

### ADM + PAT ###
ADM_PAT = [] 
for ID in range(1, 9):
    k = random.randint(0, 151)
    for i in range(k):
        ADM_PAT.append(ID)
    random.shuffle(ADM_PAT)

PAT_ADM = []
for ID in range(47, 76):
    k = random.randint(0, 112)
    for i in range(k):
        PAT_ADM.append(ID)
    random.shuffle(PAT_ADM)

links = []
for i in range(min(len(ADM_PAT), len(PAT_ADM))):
    links.append([ADM_PAT[i], PAT_ADM[i]])

AP = {}
PA = {}
count = 0
for link in links:
    i = links[count][0] # ADM ID
    j = links[count][1] # PAT ID
    if i in AP:
        AP[i] += 1
    else:
        AP[i] = 1

    if j in PA:
        PA[j] += 1
    else:
        PA[j] = 1
    count += 1
AP = list(AP.values())
PA = list(PA.values())

### MED + NUR ###
MED_NUR = [] 
for ID in range(1, 9):
    k = random.randint(23, 472)
    for i in range(k):
        MED_NUR.append(ID)
    random.shuffle(MED_NUR)

NUR_MED = []
for ID in range(20, 47):
    k = random.randint(0, 446)
    for i in range(k):
        NUR_MED.append(ID)
    random.shuffle(NUR_MED)

links = []
for i in range(min(len(MED_NUR), len(NUR_MED))):
    links.append([MED_NUR[i], NUR_MED[i]])

MN = {}
NM = {}
count = 0
for link in links:
    i = links[count][0] # MED ID
    j = links[count][1] # NUR ID
    if i in MN:
        MN[i] += 1
    else:
        MN[i] = 1

    if j in NM:
        NM[j] += 1
    else:
        NM[j] = 1
    count += 1
MN = list(MN.values())
NM = list(NM.values())

### MED + PAT ###
MED_PAT = [] 
for ID in range(1, 9):
    k = random.randint(18, 371)
    for i in range(k):
        MED_PAT.append(ID)
    random.shuffle(MED_PAT)

PAT_MED = []
for ID in range(20, 47):
    k = random.randint(0, 143)
    for i in range(k):
        PAT_MED.append(ID)
    random.shuffle(PAT_MED)

links = []
for i in range(min(len(MED_PAT), len(PAT_MED))):
    links.append([MED_PAT[i], PAT_MED[i]])

MP = {}
PM = {}
count = 0
for link in links:
    i = links[count][0] # MED ID
    j = links[count][1] # PAT ID
    if i in MP:
        MP[i] += 1
    else:
        MP[i] = 1

    if j in PM:
        PM[j] += 1
    else:
        PM[j] = 1
    count += 1
MP = list(MP.values())
PM = list(PM.values())

### NUR + PAT ###
NUR_PAT = [] 
for ID in range(1, 9):
    k = random.randint(33, 852)
    for i in range(k):
        NUR_PAT.append(ID)
    random.shuffle(NUR_PAT)

PAT_NUR = []
for ID in range(20, 47):
    k = random.randint(7, 803)
    for i in range(k):
        PAT_NUR.append(ID)
    random.shuffle(PAT_NUR)

links = []
for i in range(min(len(NUR_PAT), len(PAT_NUR))):
    links.append([NUR_PAT[i], PAT_NUR[i]])

NP = {}
PN = {}
count = 0
for link in links:
    i = links[count][0] # NUR ID
    j = links[count][1] # PAT ID
    if i in NP:
        NP[i] += 1
    else:
        NP[i] = 1

    if j in PN:
        PN[j] += 1
    else:
        PN[j] = 1
    count += 1
NP = list(NP.values())
PN = list(PN.values())


blocks = [A, AM, AN, AP,
          MA, M, MN, MP,
          NA, NM, N, NP,
          PA, PM, PN, P]


# subplot of cumulative degree distributions
plt.style.use('seaborn')

f,((ax1, ax2, ax3, ax4), 
(ax5, ax6, ax7, ax8),
(ax9, ax10, ax11, ax12),
(ax13, ax14, ax15, ax16)) = plt.subplots(4, 4, figsize = (12, 8))

axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16]

i = 0
for block in blocks:
    x = np.cumsum(block)
    y = np.arange(len(block))/float(len(block))
    axs[i].plot(x, 1-y)
    # axs[i].semilogy()
    # axs[i].semilogx()
    i += 1

axs[0].set_title('ADM')
axs[1].set_title('MED')
axs[2].set_title('NUR')
axs[3].set_title('PAT')
axs[0].set_ylabel('ADM')
axs[4].set_ylabel('MED')
axs[8].set_ylabel('NUR')
axs[12].set_ylabel('PAT')
plt.show()