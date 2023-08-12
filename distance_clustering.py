import pylab
import matplotlib.pyplot as plt
from node import Node
import numpy as np
from sklearn.cluster import KMeans

def identify_neighbours(nodesList):
    for node in nodesList:
        neigh = []
        for m in nodesList:
            if m is node:
                continue
            if ((m.grid_x-node.grid_x)**2 + (m.grid_y-node.grid_y)**2) <= (node.tran_range)**2:
                neigh.append(m)
        neigh.sort(key=lambda m: (m.grid_x-node.grid_x)**2 + (m.grid_y-node.grid_y)**2)
        node.setNeighbors(neigh)

# def distance_clustering(nodesList):

#     identify_neighbours(nodesList)
#     c_id = 1
#     for node in nodesList:
#         if node.cluster_id!=None:
#             continue
#         numm = 0
#         for ot in node.neighbor_tran_range:
#             if ot.cluster_id == None:
#                 ot.cluster_id = c_id
#                 numm+=1
#         node.cluster_id = c_id
#         node.cluster_head = True
#         c_id+=1

#     fig, ax = plt.subplots()
#     show_cluster_heads(nodesList,fig,ax)

def find_nearest(nodesList,x,y):
    d = []
    for node in nodesList:
        d.append([node,(node.grid_x-x)**2 + (node.grid_y-y)**2])
    d.sort(key=lambda x: x[1])
    return d[0][0]

def k_means(nodesList,xxx,yyy):
    identify_neighbours(nodesList)
    points = {} 
    for node in nodesList:
        points[(node.grid_x,node.grid_y)]=node
    dataset = list(points.keys())
    dataset = [[d[0],d[1]] for d in dataset]
    X = np.array(dataset)
    kmeans = KMeans(n_clusters=len(nodesList)-10,init='random', random_state=None).fit(X)
    c_id = 1
    for center in list(kmeans.cluster_centers_):
        n = find_nearest(nodesList,center[0],center[1])
        if n.cluster_id!=None:
            continue
        for ot in n.neighbor_tran_range:
            if ot.cluster_id == None:
                ot.cluster_id = c_id
        n.cluster_id = c_id
        n.cluster_head = True
        c_id+=1
    for node in nodesList:
        if node.cluster_id==None or len(node.neighbor_tran_range)==0:
            node.cluster_id = c_id
            c_id+=1
    
    no_of_clusters,alone = 0,0
    for node in nodesList:
        if node.cluster_head==True:
            no_of_clusters+=1
            if len(node.neighbor_tran_range)==0:
                no_of_clusters-=1
                alone+=1
                continue
    return no_of_clusters,alone
    
    # fig, ax = plt.subplots()
    # a,b = show_cluster_heads(nodesList,fig,ax,xxx,yyy)
    
def show_cluster_heads(nodesList,fig,ax,xxxx,yyy):
    plt.scatter([node.grid_x for node in nodesList],[node.grid_y for node in nodesList],color='y')
    no_of_clusters,alone=0,0
    for node in nodesList:
        if node.cluster_head==True:
            no_of_clusters+=1
            #ch.append(node)
            coun = 0
            for xxx in node.neighbor_tran_range:
                if xxx.cluster_id==node.cluster_id and xxx.cluster_head!=True:
                    coun+=1
            if len(node.neighbor_tran_range)==0 or coun==0:
                plt.scatter([node.grid_x],[node.grid_y],color='g')
                circle1 = plt.Circle((node.grid_x, node.grid_y), node.tran_range, color='g',fill=False)
                ax.add_artist(circle1)
                #plt.pause(0.1)
                no_of_clusters-=1
                alone+=1
                continue
            plt.scatter([node.grid_x],[node.grid_y],color='r')
            circle1 = plt.Circle((node.grid_x, node.grid_y), node.tran_range, color='r',fill=False)
            ax.add_artist(circle1)
            #plt.pause(1)
            plt.scatter([xx.grid_x for xx in node.neighbor_tran_range if xx.cluster_id==node.cluster_id and xx.cluster_head==False],[xx.grid_y for xx in node.neighbor_tran_range if xx.cluster_head==False and xx.cluster_id==node.cluster_id],color='b')
            #plt.pause(0.1)
    #plt.legend(bbox_to_anchor=(0, 1), loc='upper left', ncol=1)
    plt.title("DISTANCE BASED CLUSTERING",fontsize=10)
    plt.xlabel('X - axis')
    plt.ylabel('Y - axis')
    import matplotlib.patches as mpatches
    red_patch = mpatches.Patch(color='red', label='Cluster Head')
    b_patch = mpatches.Patch(color='blue', label='Node Assigned to a Cluster')
    g_patch = mpatches.Patch(color='green', label='Alone Node')
    plt.figtext(0.5, -0.05, "No. of Nodes = %d, Grid Size = %d x %d, No. of Clusters = %d, Alone Nodes = %d" %(len(nodesList),xxxx,yyy,no_of_clusters,alone), ha="center")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.,handles=[red_patch,b_patch,g_patch])
   # plt.show()
    return no_of_clusters,alone





