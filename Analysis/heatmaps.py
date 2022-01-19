# Creates ward heatmap, status heatmaps and 2-and-2 combination heatmaps for the entire study period 

import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

ward_arr = np.zeros((76, 76), dtype = float)

f = open('Data/weightedEdgeList.txt')

next(f) # skip the first line in the file
for line in f:
    splitLine = line.rstrip().split('\t')
    i = int(splitLine[0])
    j = int(splitLine[1])
    Si = splitLine[2]
    Sj = splitLine[3]
    Wij = int(splitLine[4])
    # ward_arr[i, j] = Wij
    # ward_arr[j, i] = Wij
    ward_arr[i, j] = np.log(Wij)
    ward_arr[j, i] = np.log(Wij)
 
f.close()

ward_arr = ward_arr+1 # unngå verdier med 0 som man ikke kan ta log av

# heatmap for the entire ward
ward_arr = ward_arr[1:76, 1:76]
ward_hm = sns.heatmap(ward_arr, vmin = 1, vmax = 8)
ward_hm.set_title('Ward')
# grid lines dividing the groups
ward_hm.axhline(8, linewidth = 1, color = 'w')
ward_hm.axhline(19, linewidth = 1, color = 'w')
ward_hm.axhline(46, linewidth = 1, color = 'w')
ward_hm.axvline(8, linewidth = 1, color = 'w')
ward_hm.axvline(19, linewidth = 1, color = 'w')
ward_hm.axvline(46, linewidth = 1, color = 'w')
plt.show()

def status_heatmap(arr, title):
    hm = sns.heatmap(arr, vmin = 0, vmax = 6)
    hm.set_title(title)
    plt.show()

# status_heatmap(ward_arr[0:8, 0:8], 'ADM')
# status_heatmap(ward_arr[8:19, 8:19], 'MED')
# status_heatmap(ward_arr[19:46, 19:46], 'NUR')
# status_heatmap(ward_arr[46:75, 46:75], 'PAT')

def combo_heatmap(arr, title, axline):
    hm = sns.heatmap(arr, vmin = 0, vmax = 6)
    hm.set_title(title)
    hm.axhline(axline, linewidth = 1, color = 'w')
    hm.axvline(axline, linewidth = 1, color = 'w')
    plt.show()

# combo_heatmap(ward_arr[0:19, 0:19], 'ADM + MED', 8)
# combo_heatmap(ward_arr[8:46, 8:46], 'MED + NUR', 11)
# combo_heatmap(ward_arr[19:75, 19:75], 'NUR + PAT', 27)

