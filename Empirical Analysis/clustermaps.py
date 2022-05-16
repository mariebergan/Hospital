# Creates clustermaps for eachs of the 4 categories

import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

ward_arr = np.zeros((75, 75), dtype = int)

f =  open('Data/weightedEdgeList.txt')
for line in f:
    splitLine = line.rstrip().split('\t')
    i = int(splitLine[0])
    j = int(splitLine[1])
    Si = splitLine[2]
    Sj = splitLine[3]
    Wij = int(splitLine[4])
    ward_arr[i, j] = np.log(Wij)
    ward_arr[j, i] = np.log(Wij)
    
f.close()

def clustermap(arr, title):
    sns.clustermap(arr, vmin = 0, vmax = 6, figsize=(8, 6)).fig.suptitle(title) 
    plt.savefig('/Users/marie/Documents/Utdanning/Bioteknologi master/MASTER/Emp_figs/clustermap' + title + '.png')
    plt.show()

clustermap(ward_arr[0:8, 0:8], 'ADM')
clustermap(ward_arr[8:19, 8:19], 'MED')
clustermap(ward_arr[19:46, 19:46], 'NUR')
clustermap(ward_arr[46:75, 46:75], 'PAT')
