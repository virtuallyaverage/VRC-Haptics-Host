import threading
import numpy as np
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
class VRCConnnectionHandler:
    def __init__(self,
                 vrc_ip: str = "127.0.0.1",
                 recv_port: int = 9001,
                 base_addr: str = "/avatar/parameters/"
                 ) -> None:
        
        self.recv_port = recv_port
        self.vrc_ip = vrc_ip
        
        self.registered_callbacks = []
        
        self.server = None
        
        # Create receiving server for vrc
        self.dispatcher = Dispatcher()
        self.dispatcher.map(f"{base_addr}*", self.handle_address)
        self.startServer()
        
    def handle_address(self, address: str, *args):
        for callback in self.registered_callbacks:
            callback(address, args)
            
    def register_callback(self, callback):
        self.registered_callbacks.append(callback)
        
    def remove_callback(self, callback) -> bool:
        if callback in self.registered_callbacks:
            self.registered_callbacks.remove(callback)
            return True
        else:
            return False
            
    def startServer(self):
        #shut down server if already running
        if self.server:
            self.server.shutdown()
            self.server_thread.join()
            
        # Create receiving server for vrc
        self.server = BlockingOSCUDPServer((self.vrc_ip, self.recv_port), self.dispatcher)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()
        
    def close(self):
        self.server.shutdown()
        self.server_thread.join()
    
class VRCBoardHandler:
    def __init__(self, 
                 collider_groups: list[tuple[str, int]],
                 ) -> None:
        #bool Parameters
        self.motors_enabled = True
        self.visuals_enabled = False
        
        # float parameters
        self.intensity_scale = 1
        self.mod_dist = 0.2
        self.mod_freq = 0.2
        
        self.num_colliders = 0
        
        # build addresses
        self.collider_addresses = self._build_collider_addresses(collider_groups=collider_groups)
        self.parameter_addresses = self._build_parameter_addresses()
        
        self.param = {**self.collider_addresses, **self.parameter_addresses}
        
        self.collider_values = np.array([float(0)] * self.num_colliders)
        
    def get_collider_addresses(self) -> list[str]:
        return self.collider_addresses
    
    def get_parameter_addresses(self) -> list[str]:
        return self.parameter_addresses
    
    #callbacks for variables
    def get_intensity(self) -> float:
        return self.intensity_scale
    
    def get_mod_dist(self) -> float:
        return self.mod_dist
    
    def get_mod_freq(self) -> float:
        return self.mod_freq * 10
    
    def vrc_callback(self, address, *args):
        print(f"VRC callback called:{address}: Args:{args}")
        """Take general address adn see if we need to update our variables

        Args:
            address (_type_): _description_
        """
        if (address in self.collider_addresses.keys()):
            self.collider_values[self.collider_addresses[address]] = args[0][0]
        elif (address in self.parameter_addresses.keys()):
            var_type, var_name = self.parameter_addresses[address]
        
            if var_type == type(args[0][0]):
                setattr(self, var_name, args[0][0])
                print(var_name, "set to:", args[0][0])
            else:
                print(f"wrong variable type at address: {address}, TYPE: {type(args[0][0])}, value: {args}")
        
    def _build_collider_addresses(self, 
                                   motor_prefix = 'h', 
                                   collider_groups = [("Front", 16), ("Back", 16)]
                                   ) -> dict[str: int]:
        """Returns a dictionary mapping addresses to their index in the motor array

        Args:
            motor_prefix (_type_): prefix past the default avatar 
            collider_groups (_type_): groups and how many motors are in them

        Returns:
            _type_: _description_
        """

        base_parameter = f"/avatar/parameters/{motor_prefix}"
        
        motor_colliders = {}
        
        # I know there has to be a linear scaling method, I don't care enough to implement it
        colliders_seen = 0
        for group, num_colliders in collider_groups:
            for list_index, group_index in zip(range(colliders_seen, colliders_seen+num_colliders), range(num_colliders)):
                motor_colliders[(f"{base_parameter}/{group}_{group_index}")] = list_index
                
            colliders_seen += num_colliders
        self.num_colliders = colliders_seen

        return motor_colliders
     
    def _build_parameter_addresses(self,
                                   parameter_prefix = "h_param",
                                   ) -> dict[str: tuple[bool, str]]:
        """parameter_addresses = {
            address: (type, variable_name)
        }
        """
        base_parameter = f"/avatar/parameters/{parameter_prefix}/"
        
        #if anything is added here make sure to intiate it to a default value in the __init__ function
        parameter_addresses = {
            f'{base_parameter}Enable': (bool, 'motors_enabled'),
            f'{base_parameter}Intensity': (float, 'intensity_scale'),
            f'{base_parameter}Mod_Freq': (float, 'mod_freq'),
            f'{base_parameter}Modulation': (float, 'mod_dist'),
        }
        
        return parameter_addresses
        
    

    
if __name__ == "__main__":
    connection = VRCConnnectionHandler()
    board = VRCBoardHandler([("Front", 16), ("Back", 16)])
    
    connection.close()
    

