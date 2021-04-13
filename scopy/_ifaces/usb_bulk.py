import usb.core
import usb.util

VID = 0x5345
PID = 0x1234

def auto_int(x):
        return int(x, 0)

class usb_bulk:
    ep_bulk_in = None 
    ep_bulk_out = None
    
    params = [
              ('--vid', auto_int, 'Scope VID'),
              ('--pid', auto_int, 'Scope PID'),
             ]
    
    def __init__(self, vid=VID, pid=PID):
        self.vid = vid
        self.pid = pid
        self._con()
    
    def _con(self):
        self.dev = usb.core.find(idVendor=self.vid, idProduct=self.pid)
        if self.dev is None:
            raise ValueError('Device {:04x}:{:04x} not found'.format(self.vid,self.pid))
        print("Found device")

        self.cfg = self.dev.get_active_configuration()
        self.intf = self.cfg[(0,0)] # FIXME

        self.ep_bulk_in = self.get_ep_bulk_in(self.intf)
        self.ep_bulk_out = self.get_ep_bulk_out(self.intf)
        
    def get_ep_bulk_out(self,intf):
        return usb.util.find_descriptor( 
                intf,
                # match the first OUT endpoint
                custom_match = \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_OUT)

    def get_ep_bulk_in(self,intf):
        return usb.util.find_descriptor(
                intf,
                # match the first IN endpoint
                custom_match = \
                lambda e: \
                    usb.util.endpoint_direction(e.bEndpointAddress) == \
                    usb.util.ENDPOINT_IN)
                
    def read(self, size=4096):
        data = self.dev.read(self.ep_bulk_in,size)
        data = data.tobytes()
        return data
 
    
    def write(self, data):
        self.dev.write(self.ep_bulk_out, data)

