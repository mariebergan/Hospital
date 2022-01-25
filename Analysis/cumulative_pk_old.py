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

blockss = [ADM_ADM, ADM_MED, ADM_NUR, ADM_PAT, 
          MED_ADM, MED_MED, MED_NUR, MED_PAT,
          NUR_ADM, NUR_MED, NUR_NUR, NUR_PAT,
          PAT_ADM, PAT_MED, PAT_NUR, PAT_PAT]

blocks = []
for block in blockss:
    block = block.sort(reverse = True)
    blocks.append(block)

# get min and max node degree in the blocks
# max_k = []
# min_k = []
# for block in blocks:
#     max_k.append(max(block))
#     min_k.append(min(block))


# subplot of cumulative degree distributions

plt.style.use('seaborn')
f,((ax1, ax2, ax3, ax4), 
(ax5, ax6, ax7, ax8),
(ax9, ax10, ax11, ax12),
(ax13, ax14, ax15, ax16)) = plt.subplots(4, 4, figsize = (10, 7))

f.suptitle('Cumulative degree distributions', fontsize = 'x-large') 
f.supylabel('Pk')
f.supxlabel('k')

axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16]

i = 0
for block in blocks:
    x = np.cumsum(block)
    y = np.arange(len(block))/float(len(block))
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

print(blocks)