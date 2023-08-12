from node import Node
from PDU import PDU
import socket
import time
from Token import Token
import pickle
import threading
import datetime
import event




class Client():

    cluster_id = None
    node_id = None
    x = None
    y = None
    que = None

    def __init__(self,nn):
        self.cluster_id = nn.cluster_id
        self.node_id = nn.nodeId
        self.x = nn.grid_x
        self.y = nn.grid_y

    def send_to_ch(self,event):
        
        host = '127.0.0.1'
        port = self.cluster_id+18000
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:
            s.connect((host,port))
            s.send(pickle.dumps(event))
            s.close()
        except:
            print("Error in Sending at ",self.cluster_id," with node",self.node_id)  




    def sense_event(self):

        host = "127.0.0.1"

        port = self.node_id+16000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(15)
        
        while True:

            c,addr = s.accept()

            #TODO: Send recvd event to CH, do nothing else.

            data = c.recv(4096)
            
            event = pickle.loads(data)
            event.setNode(self.node_id,self.x,self.y)
            
            self.send_to_ch(event)

            #tk.history.append(["Client Server",self.cluster_id,tk.token_id,tk.src,self.node_id,tk.time,tk.time.microsecond])
            #tk.add_node(self.node_id)
            #self.que.put(tk.history)

        s.close()


    def client_script(self,q):

        self.que = q

        rec_t = threading.Thread(target=self.sense_event)
        rec_t.start()
        
        
        # time.sleep(1)
        # request_t = threading.Thread(target=self.request_token)
        # request_t.start()
        

        #request_t.join()
        rec_t.join()

## client(node) - server(cluster head) ---------> client sensed event, just send the details to cluster head 