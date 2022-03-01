import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

G = nx.Graph()

for n in range(1, 9):
    G.add_node(n, status = 'ADM')

for n in range(9, 20):
    G.add_node(n, status = 'MED')

for n in range(20, 47):
    G.add_node(n, status = 'NUR')

for n in range(47, 76):
    G.add_node(n, status = 'PAT')

f =  open('Data/weightedEdgeList.txt')

next(f) # skip the first line in f
for line in f:
    splitLine = line.rstrip().split('\t')
    i = int(splitLine[0])
    j = int(splitLine[1])
    Si = splitLine[2]
    Sj = splitLine[3]
    Wij = int(splitLine[4])

    G.add_edge(i, j, weight = Wij)
 
f.close()


degree_freq = nx.degree_histogram(G)
degrees = range(len(degree_freq))
plt.figure(figsize=(8, 6)) 
plt.loglog(degrees[3:], degree_freq[3:],'go') 
plt.xlabel('Degree')
plt.ylabel('Frequency')
plt.show()