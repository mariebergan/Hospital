# Creates a subplot of the the shift heatmaps 

from matplotlib.pyplot import xticks, yticks
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

def heatmap(file, axx):

    arr = np.zeros((76, 76), dtype = int)
    f =  open(file)

    next(f) # skip first line in file
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
    hm = sns.heatmap(arr, vmin = 0, vmax = 6, 
                     ax = axx, cbar = False, 
                     xticklabels = False, yticklabels = False)
    hm.axhline(8, linewidth = 0.5, color = 'w')
    hm.axhline(19, linewidth = 0.5, color = 'w')
    hm.axhline(46, linewidth = 0.5, color = 'w')
    hm.axvline(8, linewidth = 0.5, color = 'w')
    hm.axvline(19, linewidth = 0.5, color = 'w')
    hm.axvline(46, linewidth = 0.5, color = 'w')

# subplot with dim = (5, 3)
f,((ax1, ax2, ax3), 
(ax4, ax5, ax6),
(ax7, ax8, ax9),
(ax10, ax11, ax12),
(ax13, ax14, ax15)) = plt.subplots(5, 3, sharey = True, sharex = True, figsize = (5, 5))

ax1.set_title('Morning')
ax2.set_title('Afternoon')
ax3.set_title('Night')

ax1.set_ylabel('Monday')
# ylabel kommer ikke opp ??
ax4.set_ylabel('Tuesday') 
ax7.set_ylabel('Wednesday')
ax10.set_ylabel('Thursday')
ax13.set_ylabel('Friday')

# creates heatmaps for the shifts at indicated ax
mon_afternoon = heatmap('Data/Shifts/mon_afternoon.txt', ax2)
mon_night = heatmap('Data/Shifts/mon_night.txt', ax3)
tue_morning = heatmap('Data/Shifts/tue_morning.txt', ax4)
tue_afternoon = heatmap('Data/Shifts/tue_afternoon.txt', ax5)
tue_night = heatmap('Data/Shifts/tue_night.txt', ax6)
wed_morning = heatmap('Data/Shifts/wed_morning.txt', ax7)
wed_afternoon = heatmap('Data/Shifts/wed_afternoon.txt', ax8)
wed_night = heatmap('Data/Shifts/wed_night.txt', ax9)
thur_morning = heatmap('Data/Shifts/thur_morning.txt', ax10)
thur_afternoon = heatmap('Data/Shifts/thur_afternoon.txt', ax11)
thur_night = heatmap('Data/Shifts/thur_night.txt', ax12)
fri_morning = heatmap('Data/Shifts/fri_morning.txt', ax13)

plt.show()