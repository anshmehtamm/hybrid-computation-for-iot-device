import time
import random
class Token:

    #token_id = None
    cluster_id = None
    server_send_time = None
    processed_nodes = set()
    history = []
    time = None
    src = None
    ev = None
    

    def __init__(self,c_id,eve):
        self.cluster_id = c_id
       # self.token_id = t_id
        self.processed_nodes=set()
        self.ev = eve
        self.history=[]
        
    def add_node(self,node):
        self.processed_nodes.add(node)
    
    def next(self,neigh):
        neigh = random.sample(neigh, len(neigh)) 
        for n in neigh:
            if n.cluster_id == self.cluster_id and n.nodeId not in self.processed_nodes and n.cluster_head!=True:
                return n
        return None

    def setServerSendTime(self):
        self.server_send_time = time.ctime()

