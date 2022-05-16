# Creates a histogram subplot with the 16 blocks for the individual contact with the 4 categories
# ax2 = ADM-individuals contact with MED
# ax5 = MED-individuals contact with ADM

from matplotlib import pyplot as plt

groups = ['ADM', 'MED', 'NUR', 'PAT']
groupRange = {'ADM': [0, 8], 'MED': [8, 19], 'NUR': [19, 46], 'PAT': [46, 75]}

count = {}
for g1 in groups:
    count[g1] = {}
    for g2 in groups:
        count[g1][g2] = {}
        for ID in range(groupRange[g1][0], groupRange[g1][1]):
            count[g1][g2][ID] = 0

edgeList = open('Data/edgeList.txt')
for line in edgeList:
    splitLine = line.rstrip().split('\t')
    i = int(splitLine[0])
    j = int(splitLine[1])
    Si = str(splitLine[2])
    Sj = str(splitLine[3])

    count[Si][Sj][i] += 1
    count[Sj][Si][j] += 1

edgeList.close()

plt.style.use('seaborn')

f,((ax1, ax2, ax3, ax4), 
   (ax5, ax6, ax7, ax8),
   (ax9, ax10, ax11, ax12),
   (ax13, ax14, ax15, ax16)) = plt.subplots(4, 4, figsize = (10, 7.5))

axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16]

f.supylabel('Number of individuals with x contacts')
f.supxlabel('Number of contacts')

i = 0
for g1 in groups:
    for g2 in groups:
        axs[i].hist(list(count[g1][g2].values()))
        i += 1

axs[12].set_xlabel('ADM')
axs[13].set_xlabel('MED')
axs[14].set_xlabel('NUR')
axs[15].set_xlabel('PAT')
axs[0].set_ylabel('ADM')
axs[4].set_ylabel('MED')
axs[8].set_ylabel('NUR')
axs[12].set_ylabel('PAT')
plt.tight_layout()
plt.savefig('/Users/marie/Documents/Utdanning/Bioteknologi master/MASTER/Emp_figs/IDtoGrpContacts_hist.png')
plt.show()