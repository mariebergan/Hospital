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


f =  open('Data/edgeList.txt')

next(f)
for line in f:
    value = line.split('\t')
    i = int(value[0])
    j = int(value[1])
    Si = value[2]
    Sj = value[3]
    G.add_edge(i, j)

    
f.close()

print(G)



