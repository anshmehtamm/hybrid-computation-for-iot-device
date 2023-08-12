from Token import Token
import socket
import pickle
import threading
import random
import datetime
#from excel_write_distributed import write_to_wb

class dist_Server:

    NUM_OF_TOKENS = 1
    CLIENT_PORT_CONST = 16000
    SERVER_PORT_CONST = 18000

    SERVER_LOCK = threading.Lock()

    cluster_id = None
    node_id = None
    neighbors = None
    x = None
    y = None
    
    available_tokens = list()
    in_process_tokens = set()
    completed_tokens = set()
    que = None

    

    def __init__(self,nn):
        self.cluster_id=nn.cluster_id
        self.node_id=nn.nodeId
        self.neighbors=set(nn.neighbor_tran_range)
        self.available_tokens = self.generateTokens(self.NUM_OF_TOKENS,self.cluster_id)
        self.in_process_tokens=set()
        self.completed_tokens=set()
        self.x = nn.grid_x
        self.y = nn.grid_y

    def generateTokens(self,c,c_id):
        tokens = list()
        for t_id in range(1,c+1):
            new_token = Token(t_id,c_id)
            tokens.append(new_token)
        return tokens
    
    def nextToken(self):
        #from set of available tokens: return next token to be sent
        if len(self.available_tokens)>0:
            return self.available_tokens.pop()
        # can add more tokens or return None to mark finish and end server process for sending more tokens
        return None

    def selectClient(self):
        #TODO: check for cluster id either here or init
        return random.choice(list(self.neighbors))

    def server_script(self,q):

       # print("STARTING DISTRIBUTED SERVER #",self.node_id)
        self.que = q
        listening_t = threading.Thread(target=self.receive_token)
        listening_t.start()

        # sending_t = threading.Thread(target=self.send_token)
        # sending_t.start()

       # sending_t.join()
        listening_t.join()


    def receive_token(self):
        #recieves token from client
        #can be fully processed or half processed
        #if fully processed:add to set of processed
        #if half processed: send to next unprocessed client

        host="127.0.0.1"
        port = self.cluster_id+self.SERVER_PORT_CONST
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((host,port))
        sock.listen(15)

        while True:
            client,addr = sock.accept()

            data = client.recv(4096)
            token = pickle.loads(data)
            #print("Token", token.token_id," Received at Server")
            #token.history.append(["Distributed",self.cluster_id,token.token_id,token.src,self.node_id,token.time,token.time.microsecond])

            print("EVENT%d RCVD AT SERVER"%(token.ev.ev_id))

            to_send = token.next(self.neighbors)
            

            if to_send==None:
                #print("FULLY PROCESSED TOKEN ",token.token_id)
                #add to excel
                #write_to_wb(token.hist)
                self.que.put([token.ev.ev_id,self.cluster_id,"Distributed",token.ev.totaltime])
                #print(token.history)
                #self.completed_tokens.add(token)
            else:
                time = (((self.x-to_send.grid_x)**2 + (self.y-to_send.grid_y)**2))**(1/2)
                token.ev.totaltime += time
                sending_thread = threading.Thread(target=self.st,args=((token,to_send),))
                sending_thread.start()
                sending_thread.join()

            #check data and send appropriate response
        sock.close()

    def st(self,tk1):
        tk = tk1[0]
        to_send = tk1[1]
        host = "127.0.0.1"
        port = to_send.nodeId+self.CLIENT_PORT_CONST
      #  print("Sending Token",tk.token_id," to Client ",to_send.nodeId)
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
        s.connect((host,port))
        tk.time=datetime.datetime.now()
        tk.src = self.node_id
        s.send(pickle.dumps(tk))
        s.close()
        return




    # def send_token(self):
    #     # run periodically
    #     # call nextToken for sending a token 
    #     #print("---Starting Server Sending Process of #",self.cluster_id)
    #     host = "127.0.0.1"
    #     while True:

    #         tk = self.nextToken()
    #         if tk==None:
    #             break
    #         cl = tk.next(self.neighbors)
            
    #         port = cl.nodeId+self.CLIENT_PORT_CONST
    #         #print("Sending Token ",tk.token_id, " to Client ",cl.nodeId)
    #         token_send_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #         token_send_sock.connect((host,port))
    #         #print("Succesful")
    #         tk.time=datetime.datetime.now()
    #         tk.src = self.node_id

    #         token_send_sock.send(pickle.dumps(tk))
    #         token_send_sock.close()

    #         #TODO : decide sleep or not
    #         #time.sleep(10)




    






