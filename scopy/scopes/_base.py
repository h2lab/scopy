
class _base(object):

    def __init__(self, args):
        """
            Scope initialization code here

            Parameters
            args: parameters to pass to the scope
        """
        raise NotImplementedError("Must define your scope initialisation code here")
 
    def querry_id(self):
        """
            Returns IDN as a string
        """
        raise NotImplementedError("Must define your scope initialisation code here")
        
    def arm(self, channels=[]):
        """
            Setup scope to begin capture when triggered.

            Parameters:
            channels[]: channels to record 

            Raises
            OSError – Scope isn’t connected.

            Exception – Error when arming. This method catches these and disconnects before reraising them.
        """
        raise NotImplementedError("Must define your scope initialisation code here")
        
        
    def capture(self):
        """
            FIXME add your scope trace capture code here if needed
        """
        pass
        
        
    def get_last_trace(self):
        """            
            Return the last trace captured with this scope.

            Returns
            Numpy array of the last capture trace(s) or None (connection error)
        """
        raise NotImplementedError("Must define your scope initialisation code here")   
