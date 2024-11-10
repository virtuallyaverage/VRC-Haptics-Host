from pythonosc import udp_client, osc_server
from time import time

class HapticModule:
    def __init__(self, module_config):
        self.config = module_config
        
        #commmon constants
        self.num_motors = self.config['num_motors']
        self.update_rate = self.config['serv_rate']
        self._update_spacing = 1/self.update_rate
        self.collider_groups = self.config['collider_groups']
        self.ip  = self.config['ip']
        self.port = self.config['port']
        
        #set up OSC connection
        self.connection = udp_client.SimpleUDPClient(self.config['ip'], self.config['port'])
        self.name = self.config['name']
        
        # arrays for the client
        self.last_sent_array = [int(0)] * self.num_motors
        self.int_array_to_send = [int(0)] * self.num_motors
        
        #parameters
        self.enabled = True
        self.intensity = 1.0
        
        # Mask for these motors
        self.motor_mask = [True] * self.num_motors
            
        self._last_update_pushed = time()
        
        
    def push_update_debounced(self):
        if (time()-self._last_update_pushed > self._update_spacing):
            print(f"Pushing Update to {self.config['name']}")
            #apply mask
            
            #copy to our sent
            self.last_sent_array = self.int_array_to_send
            
            #push our array
            self.connection.send_message("/h", self._compile_array(self.int_array_to_send))
            
            # upate time
            self._last_update_pushed = time()
            
    def update_outputs(self, int_array:list[int]):
        pass

    
    def _compile_array(self, float_array):
        """Compile integer array into a hex string

        Args:
            int_array (_type_): _description_

        Returns:
            List[Hex]: A hex string representation of the integer array
        """
        # Convert each integer to a zero-padded 3-digit hexadecimal string
        hex_strings = [f"{num:04x}" for num in int_array]
        
        # Concatenate all hexadecimal strings
        hex_string = ''.join(hex_strings)
        
        return hex_string
    
    def get_stats(self):
        #commmon constants
        return f"""
        Haptic Module: {self.name}
        Number of Motors: {self.num_motors}
        Update Rate: {self.update_rate}Hz
        Collider Groups, Offset: {self.collider_groups}
        Module IP: {self.ip}
        Module Recieve Port: {self.port}"""
    
    
if __name__ == "__main__":
    import json
    
    with open("example/configs/haptic_module.json", 'r') as config:
        our_module = HapticModule(json.load(config)['head'])
        
    print(our_module.get_stats())
    
    our_module.push_update_debounced()