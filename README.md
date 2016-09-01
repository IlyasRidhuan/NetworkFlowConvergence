CITS4403 Project :Flow Analysis of Transactional Networks
---------------------------------------------------------

Authors
-------
Ilyas Ridhuan, 20770816
Thomas Smoker, 20935166

Folder/File Information
-----------------------
1)  graphData: Folder of csv files used to build the graphs
    --Warning--
    The bitcoin.csv file has just under 80 000 entries don't open in excel or numbers

2)  graphImages: Folder containing the .png files of graphs that created

3)  graph_*.py: Runs the algorithm on the specified graph type and outputs an array of net network flow at each depth, a .png file of the graph and plots the flow as a function of depth.

    --Note--
    The graph_bitcoin.py does not create the image file because the graph is too large
    and complex to do in any reasonable amount of time

4)  netflow.py: Contains the actual implementation of the algorithm within the method
                limitedNetFlow.

Run Information
---------------

1) python graph_static.py : runs the algorithm through a small predetermined graph

2) python graph_random.py : runs the algorithm through a connected and unconnected stochastic graph                              that were randomly generatated

3) python graph_bitcoin.py: runs the algorithm through the graph built from the Bitcoin network
