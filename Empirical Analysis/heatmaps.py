# Creates ward heatmap, status heatmaps and 2-and-2 combination heatmaps for the entire study period

from matplotlib.pyplot import ylabel
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

ward_arr = np.zeros((75, 75), dtype = float)

f = open('Data/weightedEdgeList.txt')

for line in f:
    splitLine = line.rstrip().split('\t')
    i = int(splitLine[0])
    j = int(splitLine[1])
    Si = splitLine[2]
    Sj = splitLine[3]
    Wij = int(splitLine[4])
    ward_arr[i, j] = np.log(Wij)
    ward_arr[j, i] = np.log(Wij)
    # ward_arr[i, j] = Wij
    # ward_arr[j, i] = Wij
f.close()



ward_arr = ward_arr + 1 # unngå verdier med 0 som man ikke kan ta log av
# heatmap for the entire ward
ward_hm = sns.heatmap(ward_arr, vmin=1, vmax=8)
plt.xlabel('ADM     MED                NUR                            PAT              ')
plt.ylabel('              PAT                         NUR              MED    ADM')
for x in [8, 19, 46]:
    ward_hm.axhline(x, linewidth = 1, color = 'w')
    ward_hm.axvline(x, linewidth = 1, color = 'w')
plt.tight_layout
plt.savefig('/Users/marie/Documents/Utdanning/Bioteknologi master/MASTER/completeFigs/empHeatmap.png')
plt.show()



def status_heatmap(arr, title):
    hm = sns.heatmap(arr, vmin = 1, vmax = 8)
    hm.set_title(title)
    plt.show()

# status_heatmap(ward_arr[0:8, 0:8], 'ADM')
# status_heatmap(ward_arr[8:19, 8:19], 'MED')
# status_heatmap(ward_arr[19:46, 19:46], 'NUR')
# status_heatmap(ward_arr[46:75, 46:75], 'PAT')

def combo_heatmap(arr, title, axline):
    hm = sns.heatmap(arr, vmin = 1, vmax = 8)
    hm.set_title(title)
    hm.axhline(axline, linewidth = 1, color = 'w')
    hm.axvline(axline, linewidth = 1, color = 'w')
    plt.show()

# combo_heatmap(ward_arr[0:19, 0:19], 'ADM + MED', 8)
# combo_heatmap(ward_arr[8:46, 8:46], 'MED + NUR', 11)
# combo_heatmap(ward_arr[19:75, 19:75], 'NUR + PAT', 27)
# combo_heatmap(ward_arr[19:46, 0:8], 'ADM + NUR', 0)

