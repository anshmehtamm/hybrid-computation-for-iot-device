from node import Node
import random


def form_copy(nodesList1):
    nodesList2 = []
    for node in nodesList1:
        x = Node(node.nodeId,"Sensing")
        x.grid_x=node.grid_x
        x.grid_y=node.grid_y
        x.tran_range=node.tran_range
        x.re=node.re
        nodesList2.append(x)
    return nodesList2

def form_nodes(n,ra,ha):
    nodesList = []
    for i in range(n):
        nodesList.append(Node(i,"Sensing"))
    for i in range(ra):
        nodesList[i].nodeType='Random'
    for i in range(ha):
        nodesList[ra+i].nodeType="Halton"
    return nodesList

def form_grid_random(nodesList,grid_x,grid_y):
    for node in nodesList:
        node.setGridX(random.randint(1,grid_x))
        node.setGridY(random.randint(1,grid_y))
    return nodesList

def form_grid_haldon(nodesList,grid_x,grid_y,basex,basey):
    x = []
    y = []
    for k in range(1,len(nodesList)+1):
        i = k
        f = 1
        r = 0
        while i>0:
            f = f/basex
            r = r + f*(i%basex)
            i = i//basex
        x.append(r*grid_x)
    for k in range(1,len(nodesList)+1):
        i = k
        f = 1
        r = 0
        while i>0:
            f = f/basey
            r = r + f*(i%basey)
            i = i//basey
        y.append(r*grid_y)
    i = 0
    for node in nodesList:
        node.grid_x = x[i]
        node.grid_y = y[i]
        i+=1
    return nodesList

def identifyNeighbours(nodesList):
    for node in nodesList:
        neigh = []
        for m in nodesList:
            if m is node:
                continue
            if ((m.grid_x-node.grid_x)**2 + (m.grid_y-node.grid_y)**2) <= (node.tran_range)**2:
                neigh.append(m)
        node.setNeighbors(neigh) 

def set_tran_range(nodesList,trn):
    for node in nodesList:
        node.setTranrange(random.randint(trn,trn))
    return nodesList

def set_re(nodesList):
    for node in nodesList:
        node.setRE(random.randint(8,10))
    return nodesList