class event():

    ev_id = None
    x = 0
    y = 0
    time = None
    sensed_by = None
    src_x = None
    src_y = None
    history = []
    totaltime = 0

    def __init__(self,id,xx,yy,timestamp):
        self.ev_id,self.x,self.y,self.time = id,xx,yy,timestamp

    def getDetails(self):
        return self.ev_id,self.x,self.y,self.time

    def addtoHistory(self,n):
        history.append(n)
    
    def setNode(self,node,x,y):
        self.sensed_by = node
        self.src_x,self.src_y = x,y
    
    def getList(self):
        return [self.ev_id,self.x,self.y,self.time]
    
    def getSensed(self):
        sensed = ""
        for n in self.sensed_by:
            sensed+=str(n)
            sensed+=", "
        return sensed



