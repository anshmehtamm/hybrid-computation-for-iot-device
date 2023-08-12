import pylab
import matplotlib.pyplot as plt
import numpy as np
import random
from node import Node

#from sklearn.cluster import AgglomerativeClustering


def visualize_points(nodesList):
    plt.scatter([node.grid_x for node in nodesList],[node.grid_y for node in nodesList])
    plt.show(block=False)
    plt.pause(3)
    plt.close()

def identify_neighbours(nodesList):
    for node in nodesList:
        neigh = []
        for m in nodesList:
            if m is node:
                continue
            if ((m.grid_x-node.grid_x)**2 + (m.grid_y-node.grid_y)**2) <= (node.tran_range)**2:
                neigh.append(m)
        node.setNeighbors(neigh)

def visulaize_graph(nodesList):
    #plt.figure(2)
    fig, ax = plt.subplots()
    plt.title("GRAPH BASED CLUSTERING - No. of Nodes = %d" %(len(nodesList)))
    plt.scatter([node.grid_x for node in nodesList],[node.grid_y for node in nodesList],color='y')
    
    
    return fig,ax
    
def graph_clustering(nodesList,xxx,yyy):
    from collections import OrderedDict
    identify_neighbours(nodesList)
   # fig,ax = visulaize_graph(nodesList)
    V = []
    for node in nodesList:
        V.append([node,[node.nc,node.re,node.nodeId]])

    V = OrderedDict(sorted(V, key=lambda x: (x[1][0], x[1][1]),reverse=True))

    ds = []
    while len(V)!=0:
        u = V.popitem(last=False)
        ru = u[0].neighbor_tran_range
        ds.append(u[0])
        for nn in ru:
            try:
                del V[nn]
            except:
                o = 1
    idd = 0
    for node in ds:
        node.cluster_head=True
        node.cluster_id=idd
        for nn in node.neighbor_tran_range:
            nn.cluster_id=idd
        idd+=1
    # fig, ax = plt.subplots()
    # plt.title("GRAPH BASED CLUSTERING")
    no_of_clusters,alone = 0,0
    for node in nodesList:
        if node.cluster_head==True:
            no_of_clusters+=1
            if len(node.neighbor_tran_range)==0:
                no_of_clusters-=1
                alone+=1
                continue
    return no_of_clusters,alone



    # a,b = show_cluster_heads(nodesList,fig,ax,xxx,yyy)
    # return a,b


def show_cluster_heads(nodesList,fig,ax,xxx,yyy):
    plt.scatter([node.grid_x for node in nodesList],[node.grid_y for node in nodesList],color='y')
    no_of_clusters,alone=0,0
    
    plt.xlabel('X - axis')
    plt.ylabel('Y - axis')
    import matplotlib.patches as mpatches
    red_patch = mpatches.Patch(color='red', label='Cluster Head')
    b_patch = mpatches.Patch(color='blue', label='Node Assigned to a Cluster')
    g_patch = mpatches.Patch(color='green', label='Alone Node')
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,handles=[red_patch,b_patch,g_patch])
    plt.subplots_adjust(bottom=0.2,right=0.5)
    for node in nodesList:
        if node.cluster_head==True:
            no_of_clusters+=1
            #ch.append(node)
            if len(node.neighbor_tran_range)==0:
                plt.scatter([node.grid_x],[node.grid_y],color='g')
                circle1 = plt.Circle((node.grid_x, node.grid_y), node.tran_range, color='g',fill=False)
                ax.add_artist(circle1)
                #plt.pause(0.3)
                no_of_clusters-=1
                alone+=1
                continue
            plt.scatter([node.grid_x],[node.grid_y],color='r')
            circle1 = plt.Circle((node.grid_x, node.grid_y), node.tran_range, color='r',fill=False)
            ax.add_artist(circle1)
            #plt.pause(0.1)
            plt.scatter([xx.grid_x for xx in node.neighbor_tran_range if xx.cluster_id==node.cluster_id and xx.cluster_head==False],[xx.grid_y for xx in node.neighbor_tran_range if xx.cluster_head==False and xx.cluster_id==node.cluster_id],color='b')
            #plt.pause(0.3)
            plt.title("GRAPH BASED CLUSTERING")
    #plt.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=1)
    
    textstr = "No. of Nodes = %d, Grid Size = %d x %d, No. of Clusters = %d, Alone Nodes = %d" %(len(nodesList),xxx,yyy,no_of_clusters-alone,alone)
    plt.text(0.02, 0.1, textstr, fontsize=14, transform=plt.gcf().transFigure)
    #plt.pause(5)
    return no_of_clusters,alone
