from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import pygraphviz
import matplotlib.pyplot as plt
import logging
import networkx as nx
from bfs import limitedBFS,wrapper
from collections import deque
import pprint
import timeit
import csv

        ##########################################################################
        #                                                                        #
        # This is a python file that was run in the AWS Instance running a full  #
        # bitcoin node to traverse and build the network topology of the Bitcoin #
        # network. It uses RPC commands to query the raw transaction historical  #
        # data and from there builds the network by tracing the inputs of these  #
        # transactions to their addresses and so on. It was also used as a means #
        # to test the algorithm on a high powered machine since the instance was #
        # a r3.8xlarge EC2 instance                                              #
        #                                                                        #
        ##########################################################################


rpc_user="cits4403project"
rpc_password="xxxxxxxxxxxx"

#Connect to the aws instance's Bitcoin node running on port 8332
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(rpc_user, rpc_password))

# Select a random address from a random transaction id from a random block to be the starting transaction and address.
# address:14JThBAeM4DSXMuChoJEreY7qTzZUYx8Bp from txid:4d17a5713c5555122540dda109e8c70025076781d55008d69b076731fb786787 from Block 250 000 chosen

def crawler(maxTxDepth):
    depth = 0
    seen = deque() #queue of transactions that have to be traversed
    seen.append('4d17a5713c5555122540dda109e8c70025076781d55008d69b076731fb786787') #append initial transaction
    nodes = []
    while depth < maxTxDepth:
        if len(seen) == 0:
           break
        item = seen.popleft()
        try:
           transaction = rpc_connection.getrawtransaction(item,1) # the "1" is to decode the raw transaction
        except:
           continue
        nodes.append({u'txid':transaction.get(u'txid')})
        inList =[]
        outList =[]
        for input in transaction.get(u'vin'):
            seen.append(input.get(u'txid'))
            try:
    	       inList.append({'txIn':input.get(u'txid'),u'vout':input.get(u'vout')}) #List of input txs used to provide node info
            except:
                continue
            for a in nodes:
                if a[u'txid'] == transaction.get(u'txid'): #find dict of current transaction
                    a.update({'in':inList})

        for output in transaction.get(u'vout'):
            try:
    	       outList.append({'to':output.get(u'scriptPubKey').get(u'addresses')[0],'value':output.get(u'value')}) #List of output txs used to provide node info
            except:
    	       continue;

            for n in nodes:
                for m in n['in']:
                    try:
                        #Matching vout of input tx to n of outputs to find out the address from which input tx came from
                        if m['txIn'] == transaction.get(u'txid') and m[u'vout'] == output.get(u'n'):
                            m.update({"from":output.get(u'scriptPubKey').get(u'addresses')[0],"value":output.get(u'value')})
                    except:
                        continue
	    for b in nodes:
    		if b[u'txid'] == transaction.get(u'txid'):
    		    b.update({'out':outList})
    	depth += 1
    return nodes

print "CRAWLING........"
output = crawler(1000)
G = nx.MultiDiGraph()
print "BUILDING........"
potentialCSV= []
for i in output:
    for n in i['in']:
        if 'from' in n.keys():
	       for m in i['out']:
            	potentialCSV.append({"source":n['from'],"target":m['to'],"value":m['value']})
                #optional to build the graph here if want to do analysis on AWS
        		G.add_weighted_edges_from([(n['from'],m['to'],m['value'])])
                
#write to csv file
with open('bitcoin.csv', 'wb') as output_file:
  dict_writer = csv.DictWriter(output_file, keys)
  dict_writer.writeheader()
  dict_writer.writerows(potentialCSV)
