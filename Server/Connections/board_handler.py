import importlib.resources
import time
import threading
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

from Utils.debounce import debounce_class as debounceC
from Utils.debounce import debounce as debounce

#wrap locals in check to allow file testing
if __name__ != "__main__":
    from Modulation.modulator import BoardModulator  
    from Connections.vrc_handler import VRCBoardHandler
else:
    import importlib.util
    import sys
    
    global is_main
    is_main = True
    
    def _import_module_from_path(module_name, module_path):
        print(module_path)
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    
    Modulation_path = "D:\\Github-projects\\VRC-Haptics-Host.worktrees\\BothWayCommunication\\Server\\Modulation\\modulator.py"
    modulator = _import_module_from_path("BoardModulator", Modulation_path)
    print(modulator)
    BoardModulator = modulator.BoardModulator
    
    
class board_handler:
    def __init__(self, 
                 board_ip:str, 
                 own_ip: str,
                 name: str, 
                 recieving_port:int, 
                 sending_port: int, 
                 update_rate: int,
                 announce_disc: bool,
                 vrc_groups: list[tuple[str, int]],
                 ) -> None:
        
        # set class variables
        self.own_ip = own_ip
        self.board_ip = board_ip
        self.recv_port = recieving_port
        self.send_port = sending_port
        self.name = name
        self.announce_disc = announce_disc
        self.vrc_groups = vrc_groups
        self.num_motors = sum([ num for _, num in vrc_groups])
        
        #state manager setup
        self.state = 'NEW'
        self.was_announced = False
        
        #frequency setup
        self.update_period = 1/update_rate
        self.last_update_time = 0
        self.last_htrbt = 0 # not been pinged yet
        
        # Instantiate sub-classes
        self.vrc_board = VRCBoardHandler(collider_groups=vrc_groups)
        self.mod = BoardModulator(
            self.vrc_board.get_intensity,
            self.vrc_board.get_mod_freq,
            self.vrc_board.get_mod_dist,
            self.num_motors,
            )
            
        # Create receiving server for this device
        self.dispatcher = Dispatcher()
        self.dispatcher.map("/hrtbt", self._handle_hrtbt)
        self.server = BlockingOSCUDPServer((self.own_ip, self.recv_port), self.dispatcher)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()
        
        # create sending client for this device
        self.client = SimpleUDPClient(self.board_ip, self.send_port)
        self._ping_board()
        
    def tick(self) -> None:
        
        if self.last_htrbt != 0:
            diff = time.time() - self.last_htrbt 
            if diff > 3.0:
                self._ping_board() #debounced, we can keep pinging as long a heartbeat is out of date
                
                if self.state != 'EXPIRED' and self.state != 'DISCONNECTED':
                    self.state = 'EXPIRED'
                    if (self.announce_disc and not self.was_announced):
                        print(f"{self.name} Disconnected.")
                        self.was_announced = True   
                        
        if (self.state == 'EXPIRED'):
            self.state = 'DISCONNECTED'
        
        if self.state != 'EXPIRED' and self.state != 'DISCONNECTED':
            next_update = self.last_update_time + self.update_period
            time_till = time.time()- next_update
            if time_till > 0.001 and self.last_update_time != 0:
                print(f"Overrun on {self.name}: {time_till:06f}s over target")
                
            self.send_packet() #function will be debounced to desired rate
            self.last_update_time = time.time()
        
    @debounceC(lambda self: self.update_period)      
    def send_packet(self) -> None:
        #set to zero if disabled  
        if self.vrc_board.motors_enabled:
            modulated_array = self.mod.sin_interp(self.vrc_board.collider_values)
        else: 
            modulated_array = [float(0)] * self.num_motors
            
        # convert, compile, and send
        int_array = self.mod.float_to_int16(modulated_array)
        hex_string = self._compile_array(int_array)
        self.client.send_message("/h", hex_string) # Send update over OSC
        
    @debounce(1)
    def _ping_board(self) -> None:
        self.client.send_message('/ping', self.recv_port) # send ping after server already set up
                    
    def _compile_array(self, int_array: list[int]) -> str:
        """Compile Int array into byte string to send to device

        Args:
            int_array (list[int]): List to compile

        Returns:
            str: Byte Strings
        """
        # Convert each integer to a zero-padded 4-byte hexadecimal string
        hex_strings = [f"{num:04x}" for num in int_array]
        
        # Concatenate all hexadecimal strings
        hex_string = ''.join(hex_strings)
        
        return hex_string

    def _handle_hrtbt(self, address, *args):
        if (self.was_announced):
            print(f"{self.name} Reconnected.")
            
        self.state = 'CONNECTED'  
        self.was_announced = False
        self.last_htrbt = time.time()
        
    def _handle_ping(self, address, *args):
        self.last_htrbt = time.time() + 5 #give five second leeway for connection to get setup
        

    def close(self):
        self.server.shutdown()
        self.server_thread.join()

    
    
if __name__ == "__main__":
    
    
    handler = board_handler(
        board_ip= "192.168.1.100",
        own_ip= "192.168.1.104",
        name='vest',
        recieving_port= 1035,
        sending_port= 1025,
        update_rate= 350,
        announce_disc= True,
        vrc_groups=[("Front", 16), ("Back", 16)],
    )
    print(handler)
    
    handler.close()
    
