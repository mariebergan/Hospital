# Creates heatmaps for the morning, afternoon and night shifts over the 4 study days

import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

def shift_heatmap(file, title):

    arr = np.zeros((76, 76), dtype = int)
    f =  open(file)

    next(f) # skips first line in file
    for line in f:
        splitLine = line.rstrip().split('\t')
        i = int(splitLine[0])
        j = int(splitLine[1])
        Si = splitLine[2]
        Sj = splitLine[3]
        Wij = int(splitLine[4])
        arr[i, j] = np.log(Wij)
        arr[j, i] = np.log(Wij)
    
    f.close()

    arr = arr[1:76, 1:76]
    hm = sns.heatmap(arr, vmin = 0, vmax = 6)
    hm.set_title(title)
    hm.axhline(8, linewidth = 1, color = 'w')
    hm.axhline(19, linewidth = 1, color = 'w')
    hm.axhline(46, linewidth = 1, color = 'w')
    hm.axvline(8, linewidth = 1, color = 'w')
    hm.axvline(19, linewidth = 1, color = 'w')
    hm.axvline(46, linewidth = 1, color = 'w')
    plt.show()
    
# call on shift_heatmap function to create individual heatmaps for the different shifts
mon_afternoon = shift_heatmap('Data/Shifts/mon_afternoon.txt', 'Monday afternoon shift')
mon_night = shift_heatmap('Data/Shifts/mon_night.txt', 'Monday night shift')
tue_morning = shift_heatmap('Data/Shifts/tue_morning.txt', 'Tuesday morning shift')
tue_afternoon = shift_heatmap('Data/Shifts/tue_afternoon.txt', 'Tuesday afternoon shift')
tue_night = shift_heatmap('Data/Shifts/tue_night.txt', 'Tuesday night shift')
wed_morning = shift_heatmap('Data/Shifts/wed_morning.txt', 'Wednesday morning shift')
wed_afternoon = shift_heatmap('Data/Shifts/wed_afternoon.txt', 'Wednesday afternoon shift')
wed_night = shift_heatmap('Data/Shifts/wed_night.txt', 'Wednesday night shift')
thur_morning = shift_heatmap('Data/Shifts/thur_morning.txt', 'Thursday morning shift')
thur_afternoon = shift_heatmap('Data/Shifts/thur_afternoon.txt', 'Thursday afternoon shift')
thur_night = shift_heatmap('Data/Shifts/thur_night.txt', 'Thursday night shift')
fri_morning = shift_heatmap('Data/Shifts/fri_morning.txt', 'Friday morning shift')