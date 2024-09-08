import asyncio
import json
import time

from pythonosc.dispatcher import Dispatcher
from pythonosc import udp_client, osc_server

from Connections.vrc_handler import vrc_handler
from Connections.haptic_devices import haptic_devices

"""VRCHAT & AVATAR CONFIG--------------------------------------------------------------------------------------------"""
with open('server_config.json', 'r') as config:       #Reads Config Json and puts string into value
    full_config = json.load(config)
    print(full_config)

vest_config = full_config['vest']
server_config = full_config['server']

"""VEST CONFIG-------------------------------------------------------------------------------------------------------"""
motor_limits = vest_config['motor_limits']
total_motors = vest_config['number_motors']    #Total number of motors!

print(f"Motor Limits: {motor_limits["min"]*100}% to {motor_limits["max"]*100}%")
print(f"Number of motors: {total_motors}")

#front: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 
#Back: 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
motor_groups = {
    'Chest': list(range(0, 8, 1)) + list(range(16, 24, 1)), # 0, 1, 2, 3, 4, 5, 6, 7, + 16, 17, 18, 19, 20, 21, 22, 23, 24,
    'Spine': list(range(8, 12, 1)) + list(range(24, 28, 1)),
    'Hip':   list(range(12, 16, 1)) + list(range(28, 32, 1))
}


"""------------------------------------------------------------------------------------------------------------------"""
def clear_motor_array():
    """sets the global buffered_array to zero
    """
    global buffered_array
    buffered_array = [int(0)] * total_motors # resets buffer for next pass

vrc = vrc_handler()
devices = haptic_devices(full_config, server_config['own_ip'])

motor_mask = [True] * total_motors
clear_motor_array()

############################## VRC OSC HANDLERS ########################################

motor_max = motor_limits["max"]
motor_min = motor_limits["min"]
motor_range = motor_max - motor_min
def motor_handler(address, *args):
    """callback function that handles the motor osc messages.

    Args:
        address (string): the address that the arguments are addressed to.
    """
    global buffered_array
    scaled_val = (args[0] * motor_range + motor_min) * vrc.intensity_scale
    buffered_array[vrc.collider_addresses[address]] = int(scaled_val * 4096) # scale to 12bit integer value
    #print(f"Address:{address}\nIndex:{vrc.collider_addresses[address]}\nValue:{round(scaled_val, 3)}")
                
def check_handler(address, *args):
    """callback function to handle the cross check colliders

    Args:
        address (string): _description_
    """
    vrc.handle_checks(address, args)
    update_mask()
    
def parameter_handler(address, *args):
    """a callback handler to deal with osc messages to the parameter address

    Args:
        address (string): the full address of the message
    """
    #print(f"PARAM: {address}: {args[0]}")
    vrc.handle_params(address, args[0])
    
dispatcher = Dispatcher()
dispatcher.map("/avatar/parameters/h/*", motor_handler)       #handles haptic data after json is jogged
dispatcher.map("/avatar/parameters/h_param/*", parameter_handler) #handle our server parameters
dispatcher.map("/avatar/parameters/h_Check/*", check_handler) #handle collision checks

##################################### Mask Manipulation ##########################################

def update_mask():
    """Update the motor_mask variable according to new parameters
    """
    #default to all motors off
    global motor_mask
    set_mask(False)
    
    if vrc.motors_enabled:
        if(vrc.checks_enabled):
            #set each group of indices to the value of the parent collider;
            motor_mask = set_mask_list(motor_mask, motor_groups["Spine"], vrc.spine_triggered)
            motor_mask = set_mask_list(motor_mask, motor_groups["Hip"], vrc.hip_triggered)
            motor_mask = set_mask_list(motor_mask, motor_groups["Chest"], vrc.chest_triggered)
        
        else:
            set_mask(True)
    
    
def set_mask_list(mask, indices:list, switch_to: bool):
    """sets the boolean mask input to the switch_to conditions at indices locations

    Args:
        mask (list[bool]): list of boolean values to modify
        indices (list[int]): list of indices to modify on the mask
        switch_to (bool): boolean values to switch to

    Returns:
        list[bool]: the modified mask
    """
    for i in indices:
        mask[i] = switch_to
    return mask

       
def apply_mask(in_list, mask):
    """Apply a mask to a list. for index i in boolean mask, mask[i] = int(0.0)

    Args:
        in_list (list[int]): the list to filter
        mask (list[bool]): The mask to apply

    Returns:
        _type_: modified list with mask applied
    """
    for index, mask_val in enumerate(mask):
        if not mask_val:
            in_list[index] = int(0)
            
    return in_list
        
def set_mask(r_input: bool):
    """Set the motor_mask to a consistent boolean value

    Args:
        input (bool): the bool value to set the whole list to
    """
    global motor_mask
    motor_mask = [r_input] * total_motors

############################################ RUNTIME SETUP/MANAGEMENT ######################
def compile_array(int_array):
    # Convert each integer to a zero-padded 3-digit hexadecimal string
    hex_strings = [f"{num:04x}" for num in int_array]
    
    # Concatenate all hexadecimal strings
    hex_string = ''.join(hex_strings)
    
    return hex_string


async def buffer():
    """Infinite loop that pushes the buffered_array to the vest at the serve_rate
    """

    while True:
        global buffered_array, vest
        
        start_time = time.time()
        #TODO: need to set up per-device mask and motor values
        update_mask()
        array_to_send = apply_mask(buffered_array, motor_mask)
        array_to_send = compile_array(array_to_send)
        devices.tick({'vest':array_to_send}) 
        

ip = "127.0.0.1"
port = 9001

async def init_main():
    server = osc_server.AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    await server.create_serve_endpoint()  # Create datagram endpoint and start serving
        
    await buffer()  # Enter main loop of program
        

if __name__ == "__main__":
    try:
        asyncio.run(init_main())
        
    except KeyboardInterrupt:
        print("Closing")
        exit()