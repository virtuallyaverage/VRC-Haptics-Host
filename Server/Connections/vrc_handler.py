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
        self.address_dict = {'':[0]} # {'address': [callbacks]}
        
        self.server = None
        
        # Create receiving server for vrc
        self.dispatcher = Dispatcher()
        self.dispatcher.map(f"{base_addr}*", self.handle_address)
        self.startServer()
        
    def handle_address(self, address: str, *args):
        try:
            callbacks = self.address_dict[address]
            if callbacks:
                for callback in callbacks:
                    callback(address, *args)
        except KeyError as e: #if key not found we haven't registered a callback for it yet
            pass
    
    def sub_to_address(self, addresses: list[str], callback: callable) -> None:
        for address in addresses:
            #if empty address we don't append
            try:
                self.address_dict[address].append(callback)
            except KeyError:
                self.address_dict[address] = [callback]     
        
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
        
class VRCBoardParameters:
    def __init__(self, 
                 motors_enabled: bool,
                 visuals_enabled: bool,
                 intensity_scale: float,
                 mod_dist: float,
                 mod_freq: float) -> None:
        self.motors_enabled = motors_enabled
        self.visuals_enabled = visuals_enabled
        self.intensity_scale = intensity_scale
        self.mod_dist = mod_dist
        self.mod_freq = mod_freq  
        
    def print(self):
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")
            
    
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
        
        self.param =  list(self.collider_addresses.keys()) + list(self.parameter_addresses.keys())
        
        self.collider_values = np.array([float(0)] * self.num_colliders)
        
    def get_collider_addresses(self) -> list[str]:
        return self.collider_addresses
    
    def get_parameter_addresses(self) -> list[str]:
        return self.parameter_addresses
    
    def get_params(self) -> 'VRCBoardParameters':
        return VRCBoardParameters(
            motors_enabled=self.motors_enabled,
            visuals_enabled=self.visuals_enabled,
            intensity_scale=self.intensity_scale,
            mod_dist=self.mod_dist,
            mod_freq=self.mod_freq
        )
        
    def set_params(self, params: 'VRCBoardParameters') -> None:
        self.motors_enabled = params.motors_enabled
        self.visuals_enabled = params.visuals_enabled
        self.intensity_scale = params.intensity_scale
        self.mod_dist = params.mod_dist
        self.mod_freq = params.mod_freq
    
    #callbacks for variables
    def get_intensity(self) -> float:
        return self.intensity_scale
    
    def get_mod_dist(self) -> float:
        return self.mod_dist
    
    def get_mod_freq(self) -> float:
        return self.mod_freq * 10
    
    def vrc_callback(self, address, *args):
        """Take general address and see if we need to update our variables

        Args:
            address (_type_): _description_
        """
        if (address in self.collider_addresses.keys()):
            self.collider_values[self.collider_addresses[address]] = args[0]
        elif (address in self.parameter_addresses.keys()):
            var_type, var_name = self.parameter_addresses[address]
        
            if var_type == type(args[0]):
                setattr(self, var_name, args[0])
                print(var_name, "set to:", args[0])
            else:
                print(f"wrong variable type at address: {address}, TYPE: {type(args[0][0])}, value: {args}")
        else:
            return
        
        
    def _build_collider_addresses(self, 
                                   motor_prefix = 'h', 
                                   collider_groups = [("Front", 16), ("Back", 16)]
                                   ) -> dict[str: int]:
        """Returns a dictionary mapping addresses to their index in the motor array

        Args:
            motor_prefix (_type_): prefix past the default avatar 
            collider_groups (_type_): groups and how many motors are in them

        Returns:m
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
    import time
    import random
    import statistics
    
    messages_max = 5000
    
    connection = VRCConnnectionHandler()

    latency =[]
    def callback_func(address: str, *args):
        now = time.time_ns()
        latency[-1] = now - latency[-1]

    addresses = [f"/avatar/parameters/address_{i}" for i in range(50)]
    for address in addresses:
        num_callbacks = 5
        for _ in range(num_callbacks):
            connection.sub_to_address([address], callback_func)

    stop_event = threading.Event()

    def simulate_messages():
        while not stop_event.is_set():
            for address in addresses:
                latency.append(time.time_ns())
                connection.handle_address(address, time.time_ns())
            time.sleep(0.1)

    simulation_thread = threading.Thread(target=simulate_messages)
    simulation_thread.daemon = True
    simulation_thread.start()

    try:
        while simulation_thread.is_alive() and len(latency) < messages_max:
            simulation_thread.join(1)
            
        print(f"Average Latency over {messages_max} messages: {statistics.fmean(latency)}ns")
        raise KeyboardInterrupt("We done")
    except KeyboardInterrupt:
        print("Ctrl+C pressed, shutting down...")
        stop_event.set()
        connection.close()

