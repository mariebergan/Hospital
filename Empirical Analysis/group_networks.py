import networkx as nx
 
ADM = nx.Graph()
for n in range(1, 9):
    ADM.add_node(n)

MED = nx.Graph()
for n in range(9, 20):
    MED.add_node(n)

NUR = nx.Graph()
for n in range(20, 47):
    NUR.add_node(n)

PAT = nx.Graph()
for n in range(47, 75):
    PAT.add_node(n)

f =  open('edgeList.txt', 'r')
lines = f.readlines()

for line in lines:
    value = line.split('\t')
    t = value[0]
    i = value[1]
    j = value[2]
    Si = value[3]
    Sj = value[4]
 
    if Si == 'ADM' and Sj == 'ADM':
        ADM.add_edge(i, j)

    if Si == 'MED' and Sj == 'MED':
        MED.add_edge(i, j)
    
    if Si == 'NUR' and Sj == 'NUR':
        NUR.add_edge(i, j)
    
    if Si == 'PAT' and Sj == 'PAT':
        PAT.add_edge(i, j)

f.close()
