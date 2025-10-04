import csv
import networkx as nx
from itertools import combinations
from collections import defaultdict
import numpy as np

path = 'marvel.csv'

def normalizeAdjacencyMatrix(A):
    n = len(A)
    for j in range(len(A[0])):
        colSum = 0
        for i in range(len(A)):
            colSum += A[i][j]

        if colSum > 0:
            for i in range(len(A)):
                if A[i][j] != 0:
                    A[i][j] = A[i][j] / colSum
    return A

comic_group = defaultdict(list)
with open(path, mode='r') as file:
    reader = csv.reader(file)
    for line in reader:
        hero = line[0]
        comic = line[1]
        comic_group[comic].append(hero)

G = nx.Graph()
for heroes in comic_group.values():
    for hero1, hero2 in combinations(heroes, 2):
        if not G.has_edge(hero1, hero2):
            G.add_edge(hero1, hero2, weight=1)

print(f"The graph contains {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

nodes = list(G.nodes())

adj_matrix = [[0] * len(nodes) for _ in range(len(nodes))]

node_to_index = {node: idx for idx, node in enumerate(nodes)}

for hero1, hero2, data in G.edges(data=True):
    idx1 = node_to_index[hero1]
    idx2 = node_to_index[hero2]
    adj_matrix[idx1][idx2] = 1
    adj_matrix[idx2][idx1] = 1


A = normalizeAdjacencyMatrix(adj_matrix)

n = len(nodes)
w0 = np.full((n, 1), 1/n)  
A = np.array(A)
for i in range(90):
    if i == 0:
        Wk = np.dot(A, w0)
    else:
        Wk = np.dot(A, Wk)

print("First 5 lines of the matrix:\n")
print(Wk[:5])
print(sum(Wk)) # must be 1
