import socket

class net_tcp:
    
    params = [
              ('--ip',  str,  'scope IP address'),
              ('--port', int, 'scope listening PORT'),
             ]
    
    def __init__(self, ip, port):
        self.ip = ip 
        self.port = port
        self._con() 
        
    def _con(self, timeout=10):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(timeout)
        server_address = (self.ip, self.port)
        print('Connecting to {} port {}'.format(*server_address))
        return self.sock.connect(server_address)

    def read(self, size=16384):
        data =  self.sock.recv(size)
        return data
    
    def write(self, data):
        self.sock.send(data)
