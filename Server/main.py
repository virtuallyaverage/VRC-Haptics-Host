import asyncio
import json
import time
from pythonosc import osc_server
import traceback

from Connections.haptic_devices import haptic_devices

with open('server_config.json', 'r') as config:       #Reads Config Json and puts string into value
    full_config = json.load(config)
    print(full_config)

vest_config = full_config['vest']
server_config = full_config['server']

motor_limits = vest_config['motor_limits']
total_motors = vest_config['number_motors']    #Total number of motors!

print(f"Motor Limits: {motor_limits["min"]*100}% to {motor_limits["max"]*100}%")
print(f"Number of motors: {total_motors}")


devices = haptic_devices(full_config, server_config['own_ip'])


async def buffer():
    """Infinite loop that pushes the buffered_array to the vest at the serve_rate
    """

    while True:
        devices.tick() 
        

async def init_main():
        
    await buffer()  # Enter main loop of program
        

if __name__ == "__main__":
    try:
        asyncio.run(init_main())
        
    except KeyboardInterrupt as e:
        print("Closing")
        devices.close()
        exit()
    except Exception as e:
        traceback.print_exc()
        print("Closing")
        devices.close()
        exit()