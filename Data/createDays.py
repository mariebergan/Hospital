# Create separate data files for each of the 4 days

secondsInDay = 86400

f = open('Data/temporalEdgeList.txt')

day1 = open('Data/temporalEdgeList_Day1.txt', 'w')
day2 = open('Data/temporalEdgeList_Day2.txt', 'w')
day3 = open('Data/temporalEdgeList_Day3.txt', 'w')
day4 = open('Data/temporalEdgeList_Day4.txt', 'w')

for line in f:
    splitLine = line.rstrip().split('\t')
    t = int(splitLine[0])
    i = splitLine[1]
    j = splitLine[2]
    Si = splitLine[3]
    Sj = splitLine[4]

    if t <= secondsInDay:
        day1.write(str(t) + '\t' + i + '\t' + j + '\t' +  Si + '\t' + Sj + '\n')
    elif t <= (secondsInDay*2):
        day2.write(str(t) + '\t' + i + '\t' + j + '\t' +  Si + '\t' + Sj + '\n')
    elif t <= (secondsInDay*3):
        day3.write(str(t) + '\t' + i + '\t' + j + '\t' +  Si + '\t' + Sj + '\n')
    elif t <= (secondsInDay*4):
        day4.write(str(t) + '\t' + i + '\t' + j + '\t' +  Si + '\t' + Sj + '\n')

day1.close()
day2.close()
day3.close()
day4.close()

f.close()