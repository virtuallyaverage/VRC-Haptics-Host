import time
import threading
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
    
class board_handler:
    def __init__(self, 
                 board_ip:str, 
                 own_ip: str,
                 name: str, 
                 recieving_port:int, 
                 sending_port: int, 
                 update_rate: int,
                 announce_disc: bool
                 ) -> None:
        
        self.own_ip = own_ip
        self.board_ip = board_ip
        self.recv_port = recieving_port
        self.send_port = sending_port
        self.name = name
        self.announce_disc = announce_disc
        
        self.state = 'NEW'
        
        self.was_announced = False
        
        self.update_period = 1/update_rate
        self.last_update_time = 0
    
        self.last_htrbt = 0 # not been pinged yet
            
        # Create receiving server for this device
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/hrtbt", self._handle_hrtbt)
        self.server = BlockingOSCUDPServer((self.own_ip, self.recv_port), self.dispatcher)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()
        
        # create sending client for this device
        self.client = SimpleUDPClient(self.board_ip, self.send_port)
        self.client.send_message('/ping', self.recv_port) # send ping after server already set up
        print("Ping sent to:", self.board_ip, ':', self.send_port)
        
    def tick(self, motor_data):
        current_time = time.time()
        if current_time - self.last_update_time > self.update_period:
            self.last_update_time = current_time
            
            self.client.send_message("/h", motor_data) # Send update over OSC
           
        if self.last_htrbt != 0:
            diff = time.time() - self.last_htrbt 
            if diff > 1.5:
                self.state = 'EXPIRED'
                if (self.announce_disc and self.was_announced):
                    print(f"{self.name} Disconnected.")
                    self.was_announced = True
                    
            
            

    def _handle_hrtbt(self, address, *args):
        self.last_htrbt = time.time()
        self.state = 'CONNECTED'
        self.was_announced = False
        
    def _handle_ping(self, address, *args):
        self.last_htrbt = time.time() + 5 #give five second leeway for connection to get setup
        

    def close(self):
        self.server.shutdown()
        self.server_thread.join()

    
    
if __name__ == "__main__":
    config = {
        'board_ip': "192.168.1.100",
        'port': 1025
    }
    
    handler = board_handler(config)
    print(handler)
    
