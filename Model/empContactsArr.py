import numpy as np

contactsArray = np.zeros((75, 75), int)
day1 = np.zeros((75, 75), int)
day2 = np.zeros((75, 75), int)
day3 = np.zeros((75, 75), int)
day4 = np.zeros((75, 75), int)

secondsInDay = 86400

temporalEdgeList = open('Data/temporalEdgeList.txt')
next(temporalEdgeList)
for line in temporalEdgeList:
    splitLine = line.rstrip().split('\t')
    t = int(splitLine[0])
    i = int(splitLine[1])-1 # slik at ID starter på 0
    j = int(splitLine[2])-1
    Si = splitLine[3]
    Sj = splitLine[4]
    contactsArray[i][j] += 1
    contactsArray[j][i] += 1

    if t < secondsInDay:
        day1[i][j] += 1
        day1[j][i] += 1
    elif t < (secondsInDay*2):
        day2[i][j] += 1
        day2[j][i] += 1
    elif t < (secondsInDay*3):
        day3[i][j] += 1
        day3[j][i] += 1
    else:
        day4[i][j] += 1
        day4[j][i] += 1
    
temporalEdgeList.close()

empContactArrays = [day1, day2, day3, day4]

