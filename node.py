import socket
import time
import threading
from _thread import *
from PDU import PDU
import pickle


class Node:

    nodeId = 0
    nodeType = ''
    grid_x = -1
    grid_y = -1
    tran_range = 0 #to be set randomly = 10 #assumed
    neighbor_tran_range = []
    nc = 0
    re = 0
    cluster_head = False
    cluster_id = None
    computing = None
    #print_lock = threading.Lock()
    

    def __init__(self,nid,ntype,nn=None):
        self.nodeId = nid
        self.nodeType = ntype
        if nn!=None:
            self.cluster_id=nn.cluster_id

    def p(self):
        print("ID: \n X:%d \n Y:%d\n Tran Range:%d\n" ,(self.nodeId,self.grid_x,self.grid_y,self.tran_range))

    def setGridX(self,x):
        self.grid_x = x
    def setGridY(self,y):
        self.grid_y = y
    def setTranrange(self,st):
        self.tran_range=st
    def setNeighbors(self,neigh):
        self.neighbor_tran_range = neigh
        self.nc = len(neigh)
    def setRE(self,res):
        self.re = res
    def setCH(self,b):
        self.cluster_head=b