# Creates separate distributions for the individual contact with the 4 categories

from matplotlib import pyplot as plt

nodes = {}
count = {}
nodeList = open('Data/nodeList.txt')

next(nodeList)
for line in nodeList:
    splitLine = line.rstrip().split('\t')
    ID = int(splitLine[0])
    status = splitLine[1]
    nodes[ID] = status # dict with ID and status as key-value
    count[ID] = {'ADM': 0, 'MED': 0, 'NUR': 0, 'PAT': 0} # 2D dict with 4 categories for each node

nodeList.close()

edgeList = open('Data/edgeList.txt')

# reads through edges and increases category value for the given node if it has a contact with the category
next(edgeList)
for line in edgeList:
    splitLine = line.rstrip().split('\t')
    i = int(splitLine[0])
    j = int(splitLine[1])
    Si = splitLine[2]
    Sj = splitLine[3]
    count[i][Sj] += 1
    count[j][Si] += 1
edgeList.close()

# creates lists with number of contacts each node in a category has with each category
for node in count:
    
    AA = []
    AM = []
    AN = []
    AP = []
    for x in range(1, 9):
        AA.append(count[x]['ADM']) # list with the number of contacts each node in the ADM has with other ADM nodes
        AM.append(count[x]['MED']) 
        AN.append(count[x]['NUR'])
        AP.append(count[x]['PAT'])
    
    MA = []
    MM = []
    MN = []
    MP = []
    for x in range(9, 20):
        MA.append(count[x]['ADM'])
        MM.append(count[x]['MED'])
        MN.append(count[x]['NUR'])
        MP.append(count[x]['PAT'])
    
    NA = []
    NM = []
    NN = []
    NP = []
    for x in range(20, 47):
        NA.append(count[x]['ADM'])
        NM.append(count[x]['MED'])
        NN.append(count[x]['NUR'])
        NP.append(count[x]['PAT'])
    
    PA = []
    PM = []
    PN = []
    PP = []
    for x in range(47, 76):
        PA.append(count[x]['ADM'])
        PM.append(count[x]['MED'])
        PN.append(count[x]['NUR'])
        PP.append(count[x]['PAT'])

def hist(list, title, y, x):
    plt.hist(list, bins = 20, edgecolor = 'black')
    plt.title(title)
    plt.ylabel(y)
    plt.xlabel(x)
    plt.show()

# use created hist function to create histogram for the indicated list
hist(AA, 'ADM-ADM', '# ADM', '# contacts with ADM')
# hist(AM, 'ADM-MED', '# ADM', '# contacts with MED')
# hist(AN, 'ADM-NUR', '# ADM', '# contacts with NUR')
# hist(AP, 'ADM-PAT', '# ADM', '# contacts with PAT')

# hist(MA, 'MED-ADM', '# MED', '# contacts with ADM')
# hist(MM, 'MED-MED', '# MED', '# contacts with MED')
# hist(MN, 'MED-NUR', '# MED', '# contacts with NUR')
# hist(MP, 'MED-PAT', '# MED', '# contacts with PAT')

# hist(NA, 'NUR-ADM', '# NUR', '# contacts with ADM')
# hist(NM, 'NUR-MED', '# NUR', '# contacts with MED')
# hist(NN, 'NUR-NUR', '# NUR', '# contacts with NUR')
# hist(NP, 'NUR-PAT', '# NUR', '# contacts with PAT')

# hist(PA, 'PAT-ADM', '# PAT', '# contacts with ADM')
# hist(PM, 'PAT-MED', '# PAT', '# contacts with MED')
# hist(PN, 'PAT-NUR', '# PAT', '# contacts with NUR')
# hist(PP, 'PAT-PAT', '# PAT', '# contacts with PAT')

