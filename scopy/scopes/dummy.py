import numpy as np

from scopy.scopes._base import _base as scope_base

IP = "127.0.0.1"
PORT = 4242

VID = 0xDEAD
PID = 0xBEFF

class dummy(scope_base):
    name = "Dummy Scope"
    ifaces = {
                "net_tcp": {"ip": IP , "port": PORT },
                "usb_bulk": {"vid": VID, "pid": PID },
             }

    def __init__(self, args):
        arg1 = None
        arg2 = None
        con = None     
        # Select connection and update params if needed 
        for i in self.ifaces.keys() :
            if args.get(i) == True:
                con = i
                for p in self.ifaces[i].keys():
                    if args.get(p) != None:
                        self.ifaces[i][p] = args.get(p)  
                        
        # create connection object
        if con ==  "net_tcp":  
            arg1 = self.ifaces[con].get('ip')
            arg2 = self.ifaces[con].get('port')              
        elif con ==  "usb_bulk":
            arg1 = self.ifaces[con].get('vid')
            arg2 = self.ifaces[con].get('pid') 
        else: 
            print(con,arg1,arg2)
            raise AttributeError            
        print("Dummy connection to:", con, arg1, arg2)

    def querry_id(self):
        return "DUMMY_SCOPE-000000042"


    def arm(self, channels=[]):
        """ 
            Setup scope to begin capture when triggered.

            Raises
            OSError – Scope isn’t connected.

            Exception – Error when arming. This method catches these and disconnects before reraising them.
        """
        pass
        
        
    def get_last_trace(self):
        """            
            Return the last trace captured with this scope.

            Returns
            Numpy array of the last capture trace(s) or None (connection error)
        """
        # return the side channel leakage: here a vector of 100 float
        return np.random.rand(100)   
        
        
