import time
import struct
import json
from scopy.scopes._base import _base as scope_base
from scopy._ifaces import net_tcp
from scopy._ifaces import usb_bulk

DEBUG = 0

RUN = "RUN"
STOP = "STOP"

ACQUIRE_MODE_SAMPLE = "SAMPle"
ACQUIRE_MODE_AVERAGE = "AVERage"
ACQUIRE_MODE_PEAK = "PEAK"

ACQUIRE_DEPMEM_1K = "1K"
ACQUIRE_DEPMEM_10K = "10K"
ACQUIRE_DEPMEM_100K = "100K"
ACQUIRE_DEPMEM_1M = "1M"
ACQUIRE_DEPMEM_10M = "10M"
ACQUIRE_DEPMEM_20M = "20M"
ACQUIRE_DEPMEM_40M = "40M"

TRIGGER_MODE_EDGE = "EDGE"
TRIGGER_MODE_VIDEO = "VIDeo"
TRIGGER_MODE_PULSE = "PULSe"
TRIGGER_MODE_SLOPE =  "SLOPe"
 
TRIGGER_EDGE_SRC_CH1 = "CH1"
TRIGGER_EDGE_SRC_CH2 = "CH2"
TRIGGER_EDGE_SRC_EXT = "EXT"
TRIGGER_EDGE_SRC_EXT_5 = "EXT/5"
TRIGGER_EDGE_SRC_ACLINE = "ACLine"

TRIGGER_EDGE_COUPLING_DC = "DC"
TRIGGER_EDGE_COUPLING_AC = "AC"
TRIGGER_EDGE_COUPLING_HF = "HF"

TRIGGER_EDGE_SLOPE_RISE = "RISE"
TRIGGER_EDGE_SLOPE_FALL = "FALE"
    
    
HORIZONTAL_SCALE_2_0ns = "2.0ns"
HORIZONTAL_SCALE_5_0ns = "5.0ns"
HORIZONTAL_SCALE_10_0ns = "10.0ns"
HORIZONTAL_SCALE_20_0ns = "20.0ns"
HORIZONTAL_SCALE_50_0ns = "50.0ns"
HORIZONTAL_SCALE_100ns = "100ns"
HORIZONTAL_SCALE_200ns = "200ns"
HORIZONTAL_SCALE_500ns = "500ns"
HORIZONTAL_SCALE_1us = "1.0us" 
HORIZONTAL_SCALE_2us = "2.0us"
HORIZONTAL_SCALE_5us = "5.0us"
HORIZONTAL_SCALE_10us = "10us"
HORIZONTAL_SCALE_20us = "20us"
HORIZONTAL_SCALE_50us = "50us"
HORIZONTAL_SCALE_100us = "100us"
HORIZONTAL_SCALE_200us = "200us"
HORIZONTAL_SCALE_500us = "500us"
HORIZONTAL_SCALE_1ms = "1.0ms"
HORIZONTAL_SCALE_2ms = "2.0ms"
HORIZONTAL_SCALE_5ms = "5.0ms"
HORIZONTAL_SCALE_10ms = "10ms"
HORIZONTAL_SCALE_20ms = "20ms"
HORIZONTAL_SCALE_50ms = "50ms"
HORIZONTAL_SCALE_100ms = "100ms"
HORIZONTAL_SCALE_200ms = "200ms"
HORIZONTAL_SCALE_500ms = "500ms"
HORIZONTAL_SCALE_1_0s = "1.0s"
HORIZONTAL_SCALE_2_0s = "2.0s"
HORIZONTAL_SCALE_5_0s = "5.0s"
HORIZONTAL_SCALE_10s = "10s"
HORIZONTAL_SCALE_20s = "20s"
HORIZONTAL_SCALE_50s = "50s"
HORIZONTAL_SCALE_100s = "100s"
HORIZONTAL_SCALE_200s = "200s"
HORIZONTAL_SCALE_500s = "500s"
HORIZONTAL_SCALE_1000s = "1000s"


VID = 0x5345
PID = 0x1234
IP = "192.168.100.42"
PORT = 3000

from pprint import *
class owon_xds(scope_base):

    name = "OWON XDS"
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
        self.con = globals()[con](arg1, arg2) 


    def do_query_string(self, cmd):
        if DEBUG:
            print("> ",cmd)
        result = ""
        self.con.write(cmd.encode())
        result = self.con.read()
        if result:
            result = result.decode()
        if DEBUG:
            print("< ",result)
        return result


    def do_command(self, cmd):
        if DEBUG:
            print(">> ",cmd)
        self.con.write(cmd.encode())
        return 


    def wait_operation(self, con):
        return do_query_string(self.con, '*OPC?')
        
    def arm(self,channels=[1,2]):
        self.channels = channels
        self.set_state(state=RUN)
    
    def set_state(self, state=RUN):
        """
            Starts/stops the oscilloscope. 
            The functions of these commands are the same with those of
            Run/Stop at the front panel.
        """
        return self.do_command(':RUNning')

    def clear(self):
        return self.do_command('*RST')

    def clear(self):
        return self.do_command('*CLS')


    def wait_for_complete(self):
        return self.do_command('*WAI;*OPC?')  
      
    def query_esr(self):
        return self.do_command('*ESR?')
        
    def check_error(self):
         return self.do_command('*ECE?') 
             
    def acquire_mode(self, mode=ACQUIRE_MODE_SAMPLE):
        return self.do_command(':ACQuire:MODE {}'.format(mode))
            
    def acquire_depmem(self, mem=ACQUIRE_DEPMEM_20M):
        return self.do_command(':ACQuire:DEPMEM {}'.format(mem))
        
    def set_acquire_average_mode_count(self, count=4):
        return self.do_command(':ACQuire:AVERage:NUM {}'.format(count))

    def set_autoset(self, state="ON"):
        return self.do_command(':AUTOset {}'.format(state))

    def set_autoscale(self, state=1):
        return self.do_command(':AUTOscale {}'.format(state))

    def querry_id(self):
        IDN = self.do_query_string('*IDN?')
        return IDN

        
    def get_header(self, screen=False):
        if screen:
            src = "SCREEN"
        else:
            src = "DEPMEM"
        cmd = ':DATA:WAVE:' + src + ':HEAD?'
        self.con.write(cmd.encode())
        header = self.read_include_size(False)
        header = json.loads(header)
        return header

    def read_include_size(self, order=True):
    
        READ_SIZE = 4096
        rawdata = []
        
        # first 4 bytes indicate the number of data bytes following  
        data = self.con.read(READ_SIZE)
        if order == True:  
            to_read = struct.unpack(">L", data[:4])[0]
        else: 
            to_read = struct.unpack("<L", data[:4])[0]
            
        data = data[4:] # stripping packet size
        if DEBUG:
            print("TO READ :", to_read)
           
        if to_read <= 4:
            return None
       
        if to_read <= READ_SIZE - 4:
            return data     
            
        rawdata += data    
        while to_read - len(rawdata) > 0:
                data = self.con.read()
                rawdata += data
                if DEBUG:
                    print("TO READ : {: >8}\r".format(to_read - len(rawdata)), end='')     
 
        if DEBUG:
            print("")
            print("READ    : {: >8}".format(len(rawdata)))
            print(rawdata)
        return rawdata
 
    def get_bmp(self):
        cmd = get_data_cmd + "BMP?"
        sent = self.con.write(cmd.encode())
        rawdata = self.read_include_size(False)
        return rawdata
                            
    def get_data(self, screen=False):
        """
        The query returns the data of the deep memory channel.
        The data point is recorded as 12-bit, a point uses two bytes, little-endian byte order
        """
        
        header = self.get_header(screen)
        
        if DEBUG:
            pprint(header)
            
        get_data_cmd = ":DATA:WAVE:"
        if screen == True:
            get_data_src = 'SCREEN:'
        else:
            get_data_src = 'DEPMEM:'
        
        channels_dict = header.get("CHANNEL")
        channels_data = []
        cmd = ""
        for c in channels_dict:
            disp = c.get("DISPLAY")
            name = c.get("NAME")
            num = int(name.split("CH")[1])
            if disp in ["on","ON","On","oN"]:
                cmd = get_data_cmd + get_data_src +  name + "?"                    
                sent = self.con.write(cmd.encode())
                rawdata = self.read_include_size(False)
                data = self.rawdata_to_signed_shorts(rawdata)
                if DEBUG:
                    print("LEN DATA: {} SIGNED SHORTS: {}".format(len(rawdata), len(data)))
                channels_data.append(data)
        return channels_data


    def rawdata_to_signed_shorts(self, rawdata) :       
        # take 2 bytes and convert them to signed short using "little-endian"            
        data = []
        for idx in range(0,len(rawdata),2):
            p = bytes(rawdata[idx:idx+2])
            point = struct.unpack("<h",p)[0]
            if not idx % 20000:
                if point == 0:
                    if DEBUG:
                        print("\t Removing dummy 0 at {}".format(idx))
                    continue
            data.append(point)
        return data       
                              
    def trigger_status(self):
        return self.do_command(':TRIGger:STATUS')

    def set_trigger_single_mode(self, mode=TRIGGER_MODE_EDGE):
        """
            Select the trigger mode of single trigger.
           
            Return: The query returns the current trigger mode of single trigger 
        """
        return self.do_command(':TRIGger:SINGle:MODE {}'.format(mode))   
        
    def set_trigger_single_edge_source(self, source=TRIGGER_EDGE_SRC_EXT):
        """
            Select the source of SINGle EDGE trigger
            
            Return: The query returns "CH1", "CH2", "EXT", "EXT/5", or "ACLine"
        """
        return self.do_command(':TRIGger:SINGle:EDGE:SOURce {}'.format(source))   

    def set_trigger_single_edge_coupling(self, coupling=TRIGGER_EDGE_COUPLING_DC):
        return self.do_command(':TRIGger:SINGle:EDGE:COUPling {}'.format(coupling)) 


    def set_trigger_single_edge_slope(self, slope=TRIGGER_EDGE_SLOPE_RISE):
        return self.do_command(':TRIGger:SINGle:EDGE:SLOPe {}?'.format(slope)) 


    def set_trigger_single_edge_level(self, level="3V"):
        return self.do_command(':TRIGger:SINGle:EDGE:LEVel {}'.format(level)) 

    def set_horizontal_scale(dev,scale=HORIZONTAL_SCALE_200ns):
        return self.do_command(':HORIzontal:SCALe {}'.format(scale))  


    def set_horizontal_scale_offset(self, offset=0):
        """
            Set the Horizontal offset of the time base.
            
            <offset> Integer -10 to +10000 （horizontal offset div）
            
            Explanation:
                If the current main time base is 500 us/div, and the horizontal 
                offset is 2 div, then the horizontal
                offset time is 1.000 ms. 
                
            Example:
                The command below sets the horizontal offset of channel1 to 1 div. 
                
                :HORIzontal:OFFset 1
                The query returns horizontal offset div. If the current main time 
                base is 500 us/div, and the horizontal offset time is 1.000 ms, 
                the query below returns "2".
        """
        return self.do_command(':HORIzontal:OFFset {}'.format(offset))

    def set_channel_coupling(self, chan=1, coupling="DC"):
        return self.do_command('CHANnel{}:COUPling {}'.format(chan, coupling))

    def set_channel_scale(self, chan=1, scale=1):
        return self.do_command('CHANnel{}:SCALe {}'.format(chan, scale))

    def set_channel_position(self, chan=1, pos=1):
        return self.do_command('CHANnel{}:POSition {}'.format(chan, pos))

    def set_channel_offset(self, chan=1, offset=0):
        return self.do_command('CHANnel{}:OFFSet {}'.format(chan, offset))

    def set_channel_bandwidth(self, chan=1, bandwidth="FULL"):
        return self.do_command('CHANnel{}:BANDwidth {}'.format(chan, bandwidth))

    def capture(self):
        """
            Dummy
        """
        pass
        
    def get_last_trace(self):
        """            
            Return the last trace captured with this scope.

            Returns
            Numpy array of the last capture trace(s) or None (connection error)
        """
        wave_forms = self.get_data(screen=False)
        return wave_forms        
        
 

 
         
