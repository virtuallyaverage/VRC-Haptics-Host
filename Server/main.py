import asyncio
import json
import time
from pythonosc import osc_server
import traceback

from Connections.haptic_devices import haptic_devices

with open('server_config.json', 'r') as config:       #Reads Config Json and puts string into value
    full_config = json.load(config)
    print(full_config)

devices = haptic_devices(full_config, full_config['server']['own_ip'])


def buffer():
    """tick each of the devices registered and handle osc communciation
    """

    while True:
        devices.tick() 
        

if __name__ == "__main__":
    try:
        buffer()
        
    except KeyboardInterrupt as e:
        print("Closing")
        devices.close()
        exit()
    except Exception as e:
        traceback.print_exc()
        print("Closing")
        devices.close()
        exit()