import networkx as nx

def wrapper(func,*args,**kwargs):
    def wrapped():
        return func(*args,**kwargs)
    return wrapped

def limitedNetFlow(G,subgraph,maxDepth):
    flowArr = []
    depth = 0
    sub = set(subgraph.nodes()) #Set containing all nodes in current subgraph
    fringe = set(subgraph.nodes()) #Set containing only nodes on the current boundary of the subgraph
    while depth < maxDepth:
        neighbour = set() #Set that will contain deduplicated list of all neighbours of nodes in the fringe
        currFlow = 0

        for node in fringe:
            currFlow += G.in_degree(node,weight="weight")-G.out_degree(node,weight="weight") #Running total of inflow - outflow for each node
            neighbour |= set(G.predecessors(node))
            neighbour |= set(G.successors(node))

        fringe = neighbour - sub # make fringe equal only to nodes which are neighbours but not already in the subgraph
        print len(fringe)
        sub |= neighbour #subgraph is now the deduplicated list of subgraph and the new neighbour set
        # try is here only for the first interation where depth-1 = -1
        try:
            ## add previous flow to the current flow to get flow across current fringe. Addition is used because outflow is negative
             # and inflow is positive
            flowArr.append(currFlow+flowArr[depth-1])
        except:
            # Occurs when there is no previous flow
            flowArr.append(currFlow)

        depth += 1
    return flowArr
