import pylab
import matplotlib.pyplot as plt
import numpy as np
import random
from node import Node

# def cluster_distance(nodesList):
#     a = []
#     for node in nodesList:
#         a.append([node.grid_x,node.grid_y])
#     X = np.array(a)
#     cluster = AgglomerativeClustering(n_clusters=10,affinity='euclidean')
#     cluster.fit_predict(X)
#     plt.scatter(X[:,0],X[:,1],c=cluster.labels_,cmap='rainbow')
#     plt.show()

def identify_neighbours(nodesList):
    for node in nodesList:
        neigh = []
        for m in nodesList:
            if m is node:
                continue
            if ((m.grid_x-node.grid_x)**2 + (m.grid_y-node.grid_y)**2) <= (node.tran_range)**2:
                neigh.append(m)
        node.setNeighbors(neigh)
    
def heuristic_clustering(nodesList,xxx,yyy):


    #identify neighbours
    identify_neighbours(nodesList)
    
    #max of NC and RE
    c=0
    count_ass = 0
    no_of_nodes = len(nodesList)
    nodesList.sort(reverse=True,key=lambda x: len(x.neighbor_tran_range))
    pos = 0
    idd = 1
    while count_ass!=no_of_nodes:
        if pos==no_of_nodes:
            pos=0
        neighbour = nodesList[pos].neighbor_tran_range
        count_nc = 0
        max_re = nodesList[pos].re
        head = nodesList[pos]
        if head.cluster_id!=None:
            pos+=1
            continue
        for node in neighbour:
            if node.cluster_id==None:
                count_nc += 1

        for node in neighbour:
            if node.cluster_id!=None:
                continue
            nc = 0
            re = node.re
            for nd in node.neighbor_tran_range:
                if nd.cluster_id==None:
                    nc+=1
            if nc>count_nc and re>max_re:
                head = node
                max_re = re
                count_nc = nc

        if head is nodesList[pos]:
            head.cluster_head=True
            head.cluster_id=idd
            c+=1
            for node in neighbour:
                if node.cluster_id==None:
                    count_ass+=1
                    node.cluster_id=idd
            idd+=1
            count_ass+=1
        pos+=1
        
    no_of_clusters,alone = 0,0
    for node in nodesList:
        if node.cluster_head==True:
            no_of_clusters+=1
            if len(node.neighbor_tran_range)==0:
                no_of_clusters-=1
                alone+=1
                continue
    return no_of_clusters,alone
    #print("No. of Cluster = ",c,idd)
    #plt.figure(1)
    # fig, ax = plt.subplots()

    # plt.title("Heuristic Based Clustering - No. of Nodes = %d" %(len(nodesList)))
    # a,b = show_cluster_heads(nodesList,fig,ax,xxx,yyy)
    # return a,b


def show_cluster_heads(nodesList,fig,ax,xxx,yyy):
    plt.scatter([node.grid_x for node in nodesList],[node.grid_y for node in nodesList],color='y')
    plt.xlabel('X - axis')
    plt.ylabel('Y - axis')
    import matplotlib.patches as mpatches
    red_patch = mpatches.Patch(color='red', label='Cluster Head')
    b_patch = mpatches.Patch(color='blue', label='Node Assigned to a Cluster')
    g_patch = mpatches.Patch(color='green', label='Alone Node')
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,handles=[red_patch,b_patch,g_patch])
    plt.subplots_adjust(bottom=0.2,right=0.5)
    no_of_cluster,alone = 0,0
    for node in nodesList:
        if node.cluster_head==True:
            #ch.append(node)4
            no_of_cluster+=1
            
            if len(node.neighbor_tran_range)==0 :
                plt.scatter([node.grid_x],[node.grid_y],color='g')
                circle1 = plt.Circle((node.grid_x, node.grid_y), node.tran_range, color='g',fill=False)
                ax.add_artist(circle1)
                plt.pause(0.3)
                no_of_cluster-=1
                alone+=1
                continue
            plt.scatter([node.grid_x],[node.grid_y],color='r')
            circle1 = plt.Circle((node.grid_x, node.grid_y), node.tran_range, color='r',fill=False)
            ax.add_artist(circle1)
            plt.pause(0.1)
            plt.scatter([xx.grid_x for xx in node.neighbor_tran_range if xx.cluster_id==node.cluster_id and xx.cluster_head==False],[xx.grid_y for xx in node.neighbor_tran_range if xx.cluster_head==False and xx.cluster_id==node.cluster_id],color='b')
            plt.pause(0.3)
            plt.title("Heuristic Based Clustering")
    textstr = "No. of Nodes = %d, Grid Size = %d x %d, No. of Clusters = %d, Alone Nodes = %d" %(len(nodesList),xxx,yyy,no_of_cluster-alone,alone)
    plt.text(0.02, 0.1, textstr, fontsize=14, transform=plt.gcf().transFigure)
    #plt.figtext(0.5, -0.05, "No. of Nodes = %d, Grid Size = %d x %d, No. of Clusters = %d, Alone Nodes = %d" %(len(nodesList),xxx,yyy,no_of_cluster-alone,alone), ha="center")
    plt.pause(5)
    return no_of_cluster,alone