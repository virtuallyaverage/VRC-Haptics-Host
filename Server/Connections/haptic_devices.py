from Connections.board_handler import board_handler
from Connections.mdns import MDNSHandler

from socket import inet_ntoa

class haptic_devices:
    def __init__(self, configs, own_ip) -> None:
        self.devices = {}
        self.handlers = []
        self.configs = configs
        
        self.own_ip = own_ip
        self.current_port = 1200

        # Start mDNS scanning
        self.mdns = MDNSHandler()
        self.mdns.subscribe(self._device_detected)

    def _device_detected(self, name, device_info):
        self.devices[name] = device_info
        print(f"Connecting to: {name} at ip: {inet_ntoa(device_info['ip'])}")
        self.handlers.append(board_handler(
            inet_ntoa(device_info['ip']), 
            self.own_ip,
            name, 
            self._get_port(), 
            device_info['port'],
            update_rate = self.configs[name]['serv_rate'],
            announce_disc = True
            ))
        
    def is_connected(self, name) -> bool:
        return self.devices[name].state == 'CONNECTED'

    def tick(self, motor_data):
        # tick each handler
        for handler in self.handlers:
            handler.tick(motor_data[handler.name])
    
    def _get_port(self):
        self.current_port += 1
        return self.current_port
    
    def close(self):
        self.zeroconf.close()