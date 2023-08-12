from Token import Token
import socket
import datetime
import pickle
import threading
from openpyxl import load_workbook
from event import event

class dist_Client:

    CLIENT_PORT_CONST = 16000
    SERVER_PORT_CONST = 18000

    cluster_id = None
    node_id = None
    x = None
    y = None
    neighbors = None
    processed_token = None
    history = {}

    def __init__(self,nn):
        self.cluster_id = nn.cluster_id
        self.node_id = nn.nodeId
        self.neighbors = self.identifyNeighbours(nn.neighbor_tran_range)
        self.x = nn.grid_x
        self.y = nn.grid_y
    
    def identifyNeighbours(self,neigh):
        a = list()
        c_head = None
        for n in neigh:
            if self.cluster_id==n.cluster_id:
                if n.cluster_head==True:
                    c_head=n
                    continue
                a.append(n)
        if len(a)==0:
            a.append(c_head)
        return a


    def client_script(self):

        listen_thread = threading.Thread(target=self.receive_event)
        listen_thread.start()

        listen_thread.join()

    def send_token(self,tk):

            to_send = tk[0].next(self.neighbors)
            

            
            #self.history[event] = [to_send.node_id,time]
            
            host = "127.0.0.1"
            if to_send==None:
               # print("Sending Token  to Server ")

                port = self.cluster_id+self.SERVER_PORT_CONST
            else:
                time = (((self.x-to_send.grid_x)**2 + (self.y-to_send.grid_y)**2))**(1/2)
                tk[1].totaltime += time
                #print("Sending Token  to Node ",to_send.nodeId)
                port = to_send.nodeId+self.CLIENT_PORT_CONST

            tk = tk[0]
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
            s.connect((host,port))
            tk.time=datetime.datetime.now()
            tk.src = self.node_id
            s.send(pickle.dumps(tk))
            s.close()
            return

    def receive_event(self):
        #print("Starting Client #",self.node_id)
        host = "127.0.0.1"
        port = self.node_id+self.CLIENT_PORT_CONST

        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((host,port))

        sock.listen(10)

        while True:

            cl,addr = sock.accept()
            #process token 
            tk = cl.recv(4096)
            RECVD = pickle.loads(tk)

            eventt = None

            if type(RECVD) is event:
                
                ev = RECVD
                #print("NEW EVENT%d RCVD at NODE %d"%(ev.ev_id,self.node_id))
                eventt = ev
                tk = Token(self.cluster_id,ev)
                tk.add_node(self.node_id)

            else:
                tk = RECVD
                #print("EVENT",tk.ev.ev_id, "RECVD AT NODE ",self.node_id)
                tk.add_node(self.node_id)
                eventt = tk.ev
                
            
            sending_thread = threading.Thread(target=self.send_token,args=((tk,event),))
            sending_thread.start()
            sending_thread.join()

            #add curr node to token
            #see neighbours list and token list to which to send
            #if no one send back to server
            #to send create another thread and a socket to bind and close that temp socke
        
        

        

