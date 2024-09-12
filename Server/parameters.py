
class vrc_parameters:
    """a handler for all recieved vrc parameters and osc addresses
    """
    def __init__(self):
        
        # bool Parameters
        self.motors_enabled = True
        self.checks_enabled = False
        
        # float Parameters
        self.intensity_scale = 1.0
        self.mod_dist = 1.0 # set to zero to disable modulation
        self.mod_frequency = 1.0
        
        # checks
        self.chest_triggered = False
        self.spine_triggered = False
        self.hip_triggered = False
        
        # address dictionaries
        self.collider_addresses = self._build_collider_addresses()
        self.parameter_addresses = self._build_parameter_addresses()
        self.checks_addresses = self._build_checks_addresses()
        
    def handle_params(self, address, *args):
        try:
            var_type, var_name, var_descriptions = self.parameter_addresses[address]
        except KeyError as e:
            print(f"Parameter not expected: {address}")
            return
        
        if var_type == type(args[0]):
            setattr(self, var_name, args[0])
            print(var_name, "set to:", args[0])
        else:
            print(f"wrong variable type at address: {address}, TYPE: {type(args[0])}, value: {args}")
    
    def handle_checks(self, address, *args):
        try:
            var_type, var_name = self.checks_addresses[address]
        except KeyError as e:
            print(f"Parameter not expected: {address}")
            return
        
        if var_type == type(args[0]):
            setattr(self, var_name, args[0])
            print(var_name, "set to:", args[0])
        else:
            print(f"wrong varible type at address: {address}, TYPE: {type(args[0])}, value: {args}")
        
    def _build_collider_addresses(self, 
                                   motor_prefix = 'h', 
                                   collider_groups = [("Front", 16), ("Back", 16)]
                                   ):
        """Returns a dictionary mapping addresses to their index in the motor array

        Args:
            motor_prefix (_type_): prefix past the default avatar 
            collider_groups (_type_): _description_

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

        #print(motor_colliders)
        return motor_colliders
    
    def _build_parameter_addresses(self,
                                   parameter_prefix = "h_param",
                                   ):
        """parameter_addresses = {
            address: type
        }
        """
        base_parameter = f"/avatar/parameters/{parameter_prefix}/"
        
        #if anything is added here make sure to intiate it to a default value in the __init__ function
        parameter_addresses = {
            f'{base_parameter}Enable': (bool, 'motors_enabled', "Enable or disable output (Similar to setting intensity to 0)"),
            f'{base_parameter}Checks': (bool, 'checks_enabled', "Enable Extra Collision Colliders"),
            f'{base_parameter}Visuals': (bool, 'visuals_enabled', "Enable In-Game Visualizers"),
            f'{base_parameter}Intensity': (float, 'intensity_scale', "Final output intensity scale (0-full duty time)"),
            f'{base_parameter}Modulation': (float, 'mod_dist', "Ratio of input signal to modulated (100-0 percent of modulated signal)"),
            f'{base_parameter}Mod_Freq': (float, 'mod_frequency', "Frequency to run modulation at (1-255hz)"),
        }
        
        return parameter_addresses
    
    def _build_checks_addresses(self,
                                   parameter_prefix = "h_Check",
                                   ):
        """parameter_addresses = {
            address: (type, name)
        }
        """
        base_parameter = f"/avatar/parameters/{parameter_prefix}/"
        
        checks_addresses = {
            f'{base_parameter}Chest': (bool, 'chest_triggered'),
            f'{base_parameter}Spine': (bool, 'spine_triggered'),
            f'{base_parameter}Hip': (bool, 'hip_triggered'),
        }
        
        return checks_addresses

    
if __name__ == "__main__":
    parameters = vrc_parameters()
    print(parameters.collider_addresses)
    print(parameters.parameter_addresses)
    print(parameters.checks_addresses)
    


