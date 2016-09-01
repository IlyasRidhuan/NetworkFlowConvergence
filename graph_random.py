import networkx as nx
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pgv
from netflow import limitedNetFlow
import csv

print "Creating Connected Random Graph"
print "==============================="
G = nx.MultiDiGraph()
with open('graphData/random.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        G.add_weighted_edges_from([(int(row[0]),int(row[1]),float(row[2]))])

#Generate labels for the edges
for u,v,d in G.edges(data=True):
    d['label'] = d.get('weight','')

#Use pygraphviz to output network graph into a png file
print "Creating random.png file of Graph"
print "==============================="
A = nx.nx_agraph.to_agraph(G)
A.layout(prog='dot')
A.draw('graphImages/random.png')
print "Done"


print "Creating UnConnected Random Graph"
print "==============================="
F = nx.MultiDiGraph()
with open('graphData/randomUncon.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        F.add_weighted_edges_from([(int(row[0]),int(row[1]),float(row[2]))])

#Generate labels for the edges
for u,v,d in F.edges(data=True):
    d['label'] = d.get('weight','')

#Use pygraphviz to output network graph into a png file
print "Creating random_unconnected.png file of Graph"
print "==============================="
A = nx.nx_agraph.to_agraph(F)
A.layout(prog='dot')
A.draw('graphImages/random_unconnected.png')
print "Done"

startingNode = 1  #pick node 1 as the starting node
maxDepth = 10 #Specify max search depth
print "Calculating flow from "+str(startingNode)+" up to a maxDepth of "+str(maxDepth)
print "==============================="
totalFlowArray = limitedNetFlow(G,G.subgraph([startingNode]),maxDepth)
print "-------------------------------"
totalFlowUnconnectedArray = limitedNetFlow(F,F.subgraph([startingNode]),maxDepth)
print "Total Flow at each step is :"
print "Connected: "+str(totalFlowArray)
print "Unconncted: "+str(totalFlowUnconnectedArray)

print "Plotting Graph of total flow"
print "==============================="
#Use Matplotlib to plot the flow as a function of search depth
connected, = plt.plot(range(1,maxDepth+1),totalFlowArray,label="Connected Graph", linestyle='--')
unconnected, = plt.plot(range(1,maxDepth+1),totalFlowUnconnectedArray,label="Unconnected Graph", linewidth=4)
legend = plt.legend(handles=[connected], loc=1)
plt.ylabel('Flow')
plt.xlabel('Depth')
# Add the legend manually to the current Axes.
ax = plt.gca().add_artist(legend)

# Create another legend for the second line.
plt.legend(handles=[unconnected], loc=4)
plt.show()
