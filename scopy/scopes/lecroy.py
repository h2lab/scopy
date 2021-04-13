from struct import pack, unpack
from time import sleep, time

from scopy.scopes._base import _base as scope_base
from scopy._ifaces import net_tcp

import serial
import os


CMD_HEADER_STRUCT    = ">BBBBL"
BUFFER_SIZE = 256
CON_TIMEOUT   = 5
IP = "192.168.0.2"
PORT = 1861


class lecroy(scope_base):

    name = "Lecroy"
    ifaces = {"net_tcp": {"ip": IP , "port": PORT } }

    def __init__(self, args):
        """
            Returns
            Scope IDN

            Raises
            OSError
            Raised when there is issues connecting to the hardware, such as user not having the correct device permissions to access the hardware.
        """            
        arg1 = None
        arg2 = None
        con = None     
        # Select connection and update params if needed 
        for i in self.ifaces.keys():
            if args.get(i) == True:
                con = i
                for p in self.ifaces[i].keys():
                    if args.get(p) != None:
                        self.ifaces[i][p] = args.get(p)  
                        
        # create connection object
        if con ==  "net_tcp":  
            arg1 = self.ifaces[con].get('ip')
            arg2 = self.ifaces[con].get('port')              
        else: 
            raise AttributeError            
        self.con = globals()[con](arg1, arg2) 



    def serialize_cmd(self, cmd):
        """
        Formatting lecroy command.
        """
        cmd_header  = pack(CMD_HEADER_STRUCT,129,1,1,0,len(cmd))
        return cmd_header + cmd.encode()


    def unserialize_data(self, data_to_string=False):
        """
        Unpacking lecroy response.
        """
        data = b""
        while True:
            header = b""
            while len(header) < 8:
                header += self.con.read(8 - len(header))
            
            byte1, byte2, byte3, byte4, size = unpack(CMD_HEADER_STRUCT, header)
            
            buf = b""
            while(len(buf) < size):
                try:
                    buf += self.con.read(size - len(buf))
                except:  
                    print("Connection error, skipping trace ...")
                    return None # If we have a reception error We drop all the data
            data += buf

            # leave infinite loop if byte1 is odd
            if byte1 % 2:
                break
                
        if(data_to_string == False):
            data = data.decode('latin-1','ignore')
        else:
            data = data[16:-1]
        return [0, data]

    def querry_id(self):
        self.con.write(self.serialize_cmd("*IDN?"))
        return self.unserialize_data(data_to_string=False)

    def set_channels_state(self, channels=[1,2], state='ON'):        
        for c in channels:
            self.con.write(self.serialize_cmd("C{}:TRACE {}".format(c, state)))
                
    def set_horizontal_scale(self,scale='2 M'):
        self.con.write(self.serialize_cmd("TIME_DIV {}".format(scale)))
        
    def set_channel_position(self, chan=1, pos=1):
        self.con.write(self.serialize_cmd("C{}:VERT_POSITION {}".format(pos)))       

    def set_channel_scale(self, chan=1, scale='1.0V'):
        self.con.write(self.serialize_cmd("C{}:VOLT_DIV {}".format(scale))) 
        
    def set_channel_bandwidth(self, chan=1, bandwidth="200MHZ"):
        self.con.write(self.serialize_cmd("C{}:BANDWIDTH_LIMIT {}".format(scale)))
        
    def get_trig_mode(self, chan=1):       
        self.con.write(self.serialize_cmd('C{}:TRIG_MODE?'.format(chan)))
        return self.unserialize_data(self.con)
        
    def set_trig_mode(self, chan=1, mode='SINGLE'):
        self.con.write(self.serialize_cmd('C{}:TRIG_MODE {}'.format(chan,mode)))

    def set_trig_slope(self, chan=1, slope='POS'):
        self.con.write(self.serialize_cmd('C{}:TRIG_SLOPE {}'.format(chan,slope)))
        
    def set_trig_level(self, chan=1, trig_level=2.0):
        self.con.write(self.serialize_cmd('C{}:TRIG_LEVEL {}'.format(chan, trig_level)))
        
    def set_trig_select(self, chan=1, trig='EDGE'):
        self.con.write(self.serialize_cmd('C{}:TRIG_SELECT {}'.format(chan, trig)))

    def arm(self,channels=[1,2]):
        """            
            Setup scope to begin capture when triggered.
        """
        self.channels = channels
        self.con.write(self.serialize_cmd('ARM_ACQUISITION'))
        return        
        
    def get_last_trace(self):
        """            
            Return the last trace captured with this scope.

            Returns
            Numpy array of the last capture trace(s) or None (connection error)
        """
        wave_forms = []
        for c in channels:
            #try:
                self.con.write(self.serialize_cmd("C{}:WAVEFORM? DAT1".format(c)))
                data = self.unserialize_data(data_to_string=True)
                wave_forms.append(np.frombuffer(data[1], dtype=np.int8).astype('int8'))  
            #except:
            #    return None
        return wave_forms
   
        


        
