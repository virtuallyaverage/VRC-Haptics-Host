import asyncio
import re
import json
import socket
import time
from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server
from pythonosc import udp_client


"""VRCHAT & AVATAR CONFIG--------------------------------------------------------------------------------------------"""
with open('server_config.json', 'r') as config:       #Reads Config Json and puts string into value
    full_config = json.load(config)
    print(full_config)

vest_config = full_config['vest_config']
server_config = full_config['server_config']

"""VEST CONFIG-------------------------------------------------------------------------------------------------------"""
vest_ip = vest_config['ip']              #Vest server IP
vest_port = vest_config['port']     #Vest server port
motor_limits = [x / 100 for x in vest_config['motor_limits']]
server_rate = vest_config['serv_rate'] #target a server refresh rate
total_motors = vest_config['number_motors']    #Total number of motors!

print(f"VestIP = {vest_ip}")
print(f"VestPort = {vest_port}")
print(f"Motor Limits: {motor_limits[0]}% to {motor_limits[1]}%")
print(f"Server Message Rate = {server_rate}hz")
print(f"Number of motors: {total_motors}")

intensity_scale = 1
motors_enabled = True
checks_enabled = False

chest_triggered = False
spine_triggered = False
hip_triggered = False

#if a motor or set of motors shouldn't be triggered set the corresponding value to False

motor_mask = [True] * total_motors

#front: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 
#Back: 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
motor_groups = {
    """Describes the groups linked to each checking collider"""
    'Chest': [range(0, 8), range(16, 24)], # 0, 1, 2, 3, 4, 5, 6, 7, + 16, 17, 18, 19, 20, 21, 22, 23, 24,
    'Spine': [range(8, 12), range(24, 27)],
    'Hip':   [range(12, 15), range(27, 31)]
}

buffered_array = [float(0)] * total_motors # resets buffer for next pass

"""------------------------------------------------------------------------------------------------------------------"""

def clear_motor_array():
    """sets the global buffered_array to zero
    """
    buffered_array = [float(0)] * total_motors # resets buffer for next pass


#init vest osc connection
#try:
vest = udp_client.SimpleUDPClient(vest_ip, vest_port)
print(f'Client established on: {vest._address}:{vest._port}')
# TODO: figure out the try and except that should be used here
# mainly the one for when there are two servers running



def motor_handler(address, *args):
    """callback function that handles the motor osc messages.

    Args:
        address (string): the address that the arguments are addressed to.
    """
    global buffered_array, intensity_scale
    

    if "Front" in address or "Back" in address :
        motor_index = int(re.search(r'\d+', address).group())
        motor_val = args[0]
        
        ScaledVal = MotorMin + ((MotorMax - MotorMin) * motor_val * intensity_scale)
        # (range of values) -> scaled % from center -> scaled to intensity parameter -> offset by minimum
        
        if "Front" in address and motor_val > 0.0:
            buffered_array[motor_index] = round(ScaledVal, 3)
            
        if "Back" in address and motor_val > 0.0:
            buffered_array[motor_index + 16] = round(ScaledVal, 3)
                
def check_handler(address, *args):
    """callback function to handle the cross check colliders

    Args:
        address (string): _description_
    """
    if "Spine" in address:
        if args[0]:
            spine_triggered = True
        else:
            spine_triggered = False
    
    elif "Hip" in address:
        if args[0]:
            hip_triggered = True
        else:
            hip_triggered = False
            
    elif "Chest" in address:
        if args[0]:
            chest_triggered = True
        else:
            chest_triggered = False
            
    else:
        print(f"Unrecognized Parameter: {address} with args: {args}")
            
    update_mask()
    
def update_mask():
    """Update the motor_mask variable to the latest values in the spine_triggered, hip_triggered, and chest_triggered variables
    """
    #default to all motors off
    motor_mask = [False] * total_motors
     
    if motors_enabled:
        print("motors enabled")
        
        if(checks_enabled):
            #set each group of indices to the value of the parent collider;
            motor_mask = set_mask_list(motor_mask, motor_groups["Spine"], spine_triggered)
            motor_mask = set_mask_list(motor_mask, motor_groups["Hip"], hip_triggered)
            motor_mask = set_mask_list(motor_mask, motor_groups["Chest"], chest_triggered)
    
    
def set_mask_list(mask, indices:list, switch_to: bool):
    """sets the boolean mask input to the switch_to conditions at indices locations

    Args:
        mask (list[bool]): list of boolean values to modify
        indices (list[int]): list of indices to modify on the mask
        switch_to (bool): boolean values to switch to

    Returns:
        list[bool]: the modified mask
    """
    for index in indices:
        if 0 <= index < len(mask):
            mask[index] = switch_to
    return mask
                
def parameter_handler(address, *args):
    """a callback handler to deal with osc messages to the parameter address

    Args:
        address (string): the full address of the message
    """
    if "Enable" in address: 
        if args[0]:
            
            motors_enabled = True
            set_mask(True)
            print("haptics On")
            
        else:
            motors_enabled = False
            set_mask(False)
            print("Haptics Off")
            
    elif "Intensity" in address:
        intensity_scale = args[0]
        print(f"intensity set to :{intensity_scale}")

    elif "Visuals" in address: #not sure why we need this here `\_('.')_/`
        print("visualizers On")
        
    elif "Checks" in address:
        if args[0]:
            print("Checks enabled")
            checks_enabled = True
            #set all motors to default off
            set_mask(False)
        else:
            checks_enabled = False
            print("Checks Disabled")
            #set motor mask to true
            set_mask(True)
    else:
        print(f"Unrecognized Parameter: {address} with args: {args}")
  
haptic_frame_interval = 1/server_rate
       
def apply_mask(in_list, mask):
    """Apply a mask to a list. if the boolean list for index i, list[i] = float(0.0)

    Args:
        in_list (list[float]): the list to filter
        mask (list[bool]): The mask to apply

    Returns:
        _type_: modified list with mask applied
    """
    for index, mask_val in enumerate(mask):
        if not mask_val:
            in_list[index] = float(0.0)
            
    return in_list
        
def set_mask(input: bool):
    """Set the motor_mask to a consistent boolean value

    Args:
        input (bool): the bool value to set the whole list to
    """
    global motor_mask
    motor_mask = [input] * total_motors

print(vest)
#Async loop sends motor values after allowing them to be buffered for buffer_length
async def buffer():
    """Infinite loop that asynchronously pushes the buffered_array to the vest at the serve_rate
    """
    while True:
        global vest, buffered_array, last_time, vest_connected, motor_mask, spine_triggered, hip_triggered, chest_triggered
        
        start_time = time.time()
        
        update_mask()
        array_to_send = apply_mask(buffered_array, motor_mask)
        vest.send_message("/h", f"{array_to_send}")  # Sends buffered values
        clear_motor_array()
        
        #target frame rate
        time_passed = time.time()-start_time
        if time_passed < haptic_frame_interval:
            sleep_time = (haptic_frame_interval-time_passed)
        else:
            print(time_passed-haptic_frame_interval)
            print("MAIN LOOP OVERRUN")
            sleep_time = 0
            
        await asyncio.sleep(sleep_time)



dispatcher = Dispatcher()
dispatcher.map("/avatar/parameters/h/*", motor_handler)       #handles haptic data after json is jogged
dispatcher.map("/avatar/parameters/h_param/*", parameter_handler) #handle our server parameters
dispatcher.map("/avatar/parameters/h_Check/*", check_handler) #handle collision checks

ip = "127.0.0.1"
port = 9001

async def init_main():
    server = osc_server.AsyncIOOSCUDPServer((ip, port), dispatcher, asyncio.get_event_loop())
    transport, protocol = await server.create_serve_endpoint()  # Create datagram endpoint and start serving
    
    await buffer()  # Enter main loop of program

    transport.close()  # Clean up serve endpoint


asyncio.run(init_main())
