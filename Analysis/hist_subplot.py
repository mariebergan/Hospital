# Creates a suplot with the 16 distributions for the individual contact with the 4 categories

from matplotlib import pyplot as plt

nodes = {}
count = {}
nodeList = open('Data/nodeList.txt')

next(nodeList)
for line in nodeList:
    splitLine = line.rstrip().split('\t')
    ID = int(splitLine[0])
    status = splitLine[1]
    nodes[ID] = status
    count[ID] = {'ADM': 0, 'MED': 0, 'NUR': 0, 'PAT': 0}

nodeList.close()

edgeList = open('Data/edgeList.txt')

next(edgeList)
for line in edgeList:
    splitLine = line.rstrip().split('\t')
    i = int(splitLine[0])
    j = int(splitLine[1])
    Si = splitLine[2]
    Sj = splitLine[3]

    count[i][Sj] += 1
    count[j][Si] += 1

edgeList.close()


for node in count:
    
    AA = []
    AM = []
    AN = []
    AP = []
    for x in range(1, 9):
        AA.append(count[x]['ADM'])
        AM.append(count[x]['MED'])
        AN.append(count[x]['NUR'])
        AP.append(count[x]['PAT'])
    
    MA = []
    MM = []
    MN = []
    MP = []
    for x in range(9, 20):
        MA.append(count[x]['ADM'])
        MM.append(count[x]['MED'])
        MN.append(count[x]['NUR'])
        MP.append(count[x]['PAT'])
    
    NA = []
    NM = []
    NN = []
    NP = []
    for x in range(20, 47):
        NA.append(count[x]['ADM'])
        NM.append(count[x]['MED'])
        NN.append(count[x]['NUR'])
        NP.append(count[x]['PAT'])
    
    PA = []
    PM = []
    PN = []
    PP = []   
    for x in range(47, 76):
        PA.append(count[x]['ADM'])
        PM.append(count[x]['MED'])
        PN.append(count[x]['NUR'])
        PP.append(count[x]['PAT'])

plt.style.use('seaborn')

f,((ax1, ax2, ax3, ax4), 
(ax5, ax6, ax7, ax8),
(ax9, ax10, ax11, ax12),
(ax13, ax14, ax15, ax16)) = plt.subplots(4, 4, figsize = (12, 7))

ax1.set_title('ADM')
ax2.set_title('MED')
ax3.set_title('NUR')
ax4.set_title('PAT')

ax1.set_ylabel('# ADM')
ax5.set_ylabel('# MED')
ax9.set_ylabel('# NUR')
ax13.set_ylabel('# PAT')

ax13.set_xlabel('# contacts with ADM')
ax14.set_xlabel('# contacts with MED')
ax15.set_xlabel('# contacts with NUR')
ax16.set_xlabel('# contacts with PAT')

ax1.hist(AA, edgecolor = 'black')
ax2.hist(AM, edgecolor = 'black')
ax3.hist(AN, edgecolor = 'black')
ax4.hist(AP, edgecolor = 'black')

ax5.hist(MA, edgecolor = 'black')
ax6.hist(MM, edgecolor = 'black')
ax7.hist(MN, edgecolor = 'black')
ax8.hist(MP, edgecolor = 'black')

ax9.hist(NA, edgecolor = 'black')
ax10.hist(NM, edgecolor = 'black')
ax11.hist(NN, edgecolor = 'black')
ax12.hist(NP, edgecolor = 'black')

ax13.hist(PA, edgecolor = 'black')
ax14.hist(PM, edgecolor = 'black')
ax15.hist(PN, edgecolor = 'black')
ax16.hist(PP, edgecolor = 'black')

plt.tight_layout()
plt.show()