import networkx as nx
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pgv
from netflow import limitedNetFlow,wrapper
import csv
import timeit

print "Creating Bitcoin Graph"
print "==============================="

G = nx.MultiDiGraph()
with open('graphData/bitcoin.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        G.add_weighted_edges_from([(row[0],row[1],float(row[2]))])

#Generate labels for the edges
for u,v,d in G.edges(data=True):
    d['label'] = d.get('weight','')

print "Creating bitcoin.png file of Graph"
print "==============================="
#CANNOT RUN BECAUSE GRAPH IS TOO BIG ~80 000 edges
# A = nx.nx_agraph.to_agraph(G)
# A.layout(prog='dot')
# A.draw('graphImages/bitcoin.png')
# print "Done"

startingNode = '14JThBAeM4DSXMuChoJEreY7qTzZUYx8Bp'  #pick address 14JThBAeM4DSXMuChoJEreY7qTzZUYx8Bp as the starting node
maxDepth = 20 #Specify max search depth
print "Calculating flow from "+str(startingNode)+" up to a maxDepth of "+str(maxDepth)
print "==============================="
totalFlowArray = limitedNetFlow(G,G.subgraph([startingNode]),maxDepth)
print "Total Flow at each step is :"
print totalFlowArray

print "Plotting Graph of total flow"
print "==============================="
#Use Matplotlib to plot the flow as a function of search depth
plt.plot(range(1,maxDepth+1),totalFlowArray)
plt.ylabel('Flow')
plt.xlabel('Depth')
plt.show()
