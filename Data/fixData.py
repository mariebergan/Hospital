def nodeList():
    f = open('Data/nodeList.txt')
    newFile = open('Data/nodeList2.txt', 'w')
    for line in f:
        splitLine = line.rstrip().split('\t')
        ID = int(splitLine[0])
        newID = ID - 1
        status = splitLine[1]
        k = splitLine[2]
        newFile.write(str(newID) + '\t' + status + '\t' + k + '\n')
    newFile.close()
    f.close()

def edgeList():
    f = open('Data/weightedEdgeList.txt')
    newFile = open('Data/weightedEdgeList2.txt', 'w')
    for line in f:
        splitLine = line.rstrip().split('\t')
        i = int(splitLine[0])
        j = int(splitLine[1])
        Si = splitLine[2]
        Sj = splitLine[3]
        Wij = splitLine[4]
        newI = i - 1
        newJ = j - 1
        newFile.write(str(newI) + '\t' + str(newJ) + '\t' + Si + '\t' + Sj + '\t' + Wij + '\n')
    newFile.close()
    f.close()
edgeList()
