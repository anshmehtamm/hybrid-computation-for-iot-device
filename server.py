import socket
from node import Node
import threading 
from _thread import *
import pickle
from PDU import PDU
import matplotlib.pyplot as plt
from Token import Token

import datetime
import event


class Server():

    print_lock = threading.Lock()
    cluster_id = None
    node_id = None
    sensed_events = []
    que = None
    x = None
    y = None

    def __init__(self,nn):
        self.cluster_id = nn.cluster_id
        self.node_id = nn.nodeId
        self.x = nn.grid_x
        self.y = nn.grid_y

    # def send_t(self,ob):
    #     host = "127.0.0.1"
    #     dest_node_id = ob.src_node_id
    #     port = dest_node_id+15000
    #   #  print(dest_node_id)
    #     s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    #     s.connect((host,port))

    #     new_token = Token(1,self.cluster_id)
    #     new_token.time=datetime.datetime.now()
    #     new_token.src = self.node_id
    #     s.send(pickle.dumps(new_token))
    #     s.close()

    def rec_event(self):

        host = ""
        port = self.cluster_id+18000
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        s.bind((host, port))
        s.listen(15)
        
        while True:

            c,addr = s.accept()

            data = c.recv(4096)
            event = pickle.loads(data)
        
            #add to sensed events with details of which client sensed.
            self.sensed_events.append(event)
            
            from_x,from_y = event.src_x,event.src_y
            time = ((self.x-from_x)**2+(self.y-from_y)**2)**(1/2)
            event.totaltime += time
            self.que.put([event.ev_id,self.cluster_id,"Client/Server",time])

            # send_token = threading.Thread(target=self.send_t,args=((ob),))
            # send_token.start()
            # send_token.join()
            # #print("Recieved from ",ob.src_cid," at",self.cluster_id)

        s.close()



    def server_script(self,q):

        self.que = q
        rec_t = threading.Thread(target=self.rec_event)
        rec_t.start()
    
        

