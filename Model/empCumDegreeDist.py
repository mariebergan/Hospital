from matplotlib import pyplot as plt
import numpy as np
from collections import Counter

groups = ['ADM', 'MED', 'NUR', 'PAT']
tab = {}
for g1 in groups:
    tab[g1] = {}
    for g2 in groups:
        tab[g1][g2] = []

edgeList = open('Data/edgeList.txt')
next(edgeList)
for line in edgeList:
    splitLine = line.rstrip().split('\t')
    i = int(splitLine[0])
    j = int(splitLine[1])
    Si = splitLine[2]
    Sj = splitLine[3]
    tab[Si][Sj].append(i)
    tab[Sj][Si].append(j)
edgeList.close()

empDegrees = {}
for g1 in groups:
    empDegrees[g1] = {}
    for g2 in groups:
        occurences = Counter(tab[g1][g2])
        empDegrees[g1][g2] = list(occurences.values())
        # add nodes with k = 0
        if g1 == 'ADM' and len(empDegrees['ADM'][g2]) < 8:
            empDegrees['ADM'][g2].extend([0 for i in range(8-len(empDegrees['ADM'][g2]))])
        if g1 == 'MED' and len(empDegrees['MED'][g2]) < 11:
            empDegrees['MED'][g2].extend([0 for i in range(11-len(empDegrees['MED'][g2]))])
        if g1 == 'NUR' and len(empDegrees['NUR'][g2]) < 27:
            empDegrees['NUR'][g2].extend([0 for i in range(27-len(empDegrees['NUR'][g2]))])
        if g1 == 'PAT' and len(empDegrees['PAT'][g2]) < 29:
            empDegrees['PAT'][g2].extend([0 for i in range(29-len(empDegrees['PAT'][g2]))])
        empDegrees[g1][g2].sort()

print(empDegrees)

k_tot = {}
for g1 in groups:
    k_tot[g1] = {}
    for g2 in groups:
        tot = sum(empDegrees[g1][g2]) 
        k_tot[g1][g2] = tot

# Cumulative degree distributions
plt.style.use('seaborn')
f,((ax1, ax2, ax3, ax4), 
(ax5, ax6, ax7, ax8),
(ax9, ax10, ax11, ax12),
(ax13, ax14, ax15, ax16)) = plt.subplots(4, 4, figsize = (12, 7.5))
f.suptitle('Cumulative degree distributions', fontsize = 'x-large') 
f.supylabel('Frequency')
f.supxlabel('Degree')
axs = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11, ax12, ax13, ax14, ax15, ax16]
logx_axs = [ax1, ax2, ax3, ax5, ax11, ax13]
logy_axs = [ax2, ax4, ax5, ax7, ax8, ax9, ax10, ax12, ax14, ax15, ax16]

i = 0
for g1 in groups:
    for g2 in groups:
        x = empDegrees[g1][g2]
        y = np.arange(len(empDegrees[g1][g2]))/float(len(empDegrees[g1][g2]))
        axs[i].plot(x, 1-y)
        for ax in logx_axs:
            ax.semilogx()
        for ax in logy_axs:
            ax.semilogy()
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
#plt.show()

