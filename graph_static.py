import networkx as nx
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pgv
from netflow import limitedNetFlow
import csv

print "Creating Deterministic Graph"
print "==============================="

G = nx.MultiDiGraph()
with open('graphData/static.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        G.add_weighted_edges_from([(int(row[0]),int(row[1]),float(row[2]))])

#Generate labels for the edges
for u,v,d in G.edges(data=True):
    d['label'] = d.get('weight','')

print "Creating random.png file of Graph"
print "==============================="
A = nx.nx_agraph.to_agraph(G)
A.layout(prog='dot')
A.draw('graphImages/static.png')
print "Done"

startingNode = 1  #pick node 1 as the starting node
maxDepth = 3 #Specify max search depth
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
