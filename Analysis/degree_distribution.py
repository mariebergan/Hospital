from matplotlib import pyplot as plt
import numpy as np

count = {}
nodeList = open('Data/nodeList.txt')

next(nodeList)
for line in nodeList:
    splitLine = line.rstrip().split('\t')
    ID = int(splitLine[0])
    status = splitLine[1]
    count[ID] = {'ADM': 0, 'MED': 0, 'NUR': 0, 'PAT': 0} 

nodeList.close()

edgeList = open('Data/edgeList.txt')

next(edgeList)
# goes through edges and counts the number of contacts each node has with nodes from each of the 4 groups 
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
    
    ADM_ADM = []
    ADM_MED = []
    ADM_NUR = []
    ADM_PAT = []

    MED_ADM = []
    MED_MED = []
    MED_NUR = []
    MED_PAT = []

    NUR_ADM = []
    NUR_MED = []
    NUR_NUR = []
    NUR_PAT = []

    PAT_ADM = []
    PAT_MED = []
    PAT_NUR = []
    PAT_PAT = []

    for x in range(1, 9):
        ADM_ADM.append(count[x]['ADM']) 
        ADM_MED.append(count[x]['MED']) 
        ADM_NUR.append(count[x]['NUR'])
        ADM_PAT.append(count[x]['PAT'])

    for x in range(9, 20):
        MED_ADM.append(count[x]['ADM'])
        MED_MED.append(count[x]['MED'])
        MED_NUR.append(count[x]['NUR'])
        MED_PAT.append(count[x]['PAT'])

    for x in range(20, 47):
        NUR_ADM.append(count[x]['ADM'])
        NUR_MED.append(count[x]['MED'])
        NUR_NUR.append(count[x]['NUR'])
        NUR_PAT.append(count[x]['PAT'])

    for x in range(47, 76):
        PAT_ADM.append(count[x]['ADM'])
        PAT_MED.append(count[x]['MED'])
        PAT_NUR.append(count[x]['NUR'])
        PAT_PAT.append(count[x]['PAT'])

blocks = [ADM_ADM, ADM_MED, ADM_NUR, ADM_PAT, 
          MED_ADM, MED_MED, MED_NUR, MED_PAT,
          NUR_ADM, NUR_MED, NUR_NUR, NUR_PAT,
          PAT_ADM, PAT_MED, PAT_NUR, PAT_PAT]

# get max node degree in the different blocks
max_k = []
min_k = []
for block in blocks:
    max_k.append(max(block))
    min_k.append(min(block))

print(max_k, min_k)


# subplot of cumulative degree distributions

plt.style.use('seaborn')

f,((ax1, ax2, ax3, ax4), 
(ax5, ax6, ax7, ax8),
(ax9, ax10, ax11, ax12),
(ax13, ax14, ax15, ax16)) = plt.subplots(4, 4, figsize = (12, 8))

axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16]
# titles = ['ADM-ADM', 'ADM-MED', 'ADM-NUR', 'ADM-PAT',
#           'MED-ADM', 'MED-MED', 'MED-NUR', 'MED-PAT',
#           'NUR-ADM', 'NUR-MED', 'NUR-NUR', 'NUR-PAT',
#           'PAT-ADM', 'PAT-MED', 'PAT-NUR', 'PAT-PAT']

# create subplot for cumulative degree distributions

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

plt.ylabel('Pk')
plt.xlabel('k')

plt.show()  

