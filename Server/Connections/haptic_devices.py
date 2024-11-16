from Connections.board_handler import board_handler
from Connections.mdns import MDNSHandler
from Connections.vrc_handler import VRCConnnectionHandler

from socket import inet_ntoa

class haptic_devices:
    def __init__(self, configs, own_ip) -> None:
        self.devices = {}
        self.handlers = {}
        self.configs = configs
        
        self.own_ip = own_ip
        self.current_port = 1200
        
        self.vrc = VRCConnnectionHandler()

        # Start mDNS scanning
        self.mdns = MDNSHandler()
        self.mdns.subscribe(self._device_detected, self._device_removed, self._device_changed)

    # Mdns Callback
    def _device_detected(self, name, device_info):
        print(f"Connecting to: {name} at ip: {inet_ntoa(device_info['ip'])}")
        self._create_device(name, device_info)
        
    # Mdns Callback
    def _device_removed(self, name):
        print(f"Removing Device: {name}")
        self.delete_device(name)
        
    # Mdns Callback
    def _device_changed(self, info, name):
        print(f"Device {name} Changed")
        #name of device deleted
        name = info.server.split('.')[0]
        params = self.handlers[name].vrc_board.get_params()
        params.print()
        
        #delete old device
        self.delete_device(name)
        
        #get updated settings
        new_device = {
            'ip': info.addresses[0],
            'port': 1027,
            'name': info.name
        }
        
        # Start so fresh so clean
        self._create_device(name, new_device)
        
        #push old config
        self.handlers[name].vrc_board.set_params(params)
            
    def _create_device(self, name, device_info):
        print(f"Creating device: {name}")
        self.devices[name] = device_info
        
        self.handlers[name] = board_handler(
            inet_ntoa(device_info['ip']), 
            self.own_ip,
            name, 
            self._get_port(), 
            device_info['port'],
            update_rate = self.configs[name]['serv_rate'],
            announce_disc = True,
            vrc_groups=self.configs[name]['vrc_groups'],
            timeout_delay=self.configs['server']['timeout_delay'],
            motor_limits=self.configs[name]['motor_limits'],
            mac = device_info['mac']
            )
        params = self.handlers[name].vrc_board.get_params()
        params.print()
        
        self.vrc.sub_to_address(self.handlers[name].vrc_board.param, self.handlers[name].vrc_board.vrc_callback)

    def delete_device(self, name: str):
        print(f"Removing device: {name}")
        self.handlers[name].close()
        del self.handlers[name]
        del self.devices[name]
        
    def is_connected(self, name) -> bool:
        return self.devices[name].state == 'CONNECTED'

    def tick(self):
        # tick each handler
        try:
            for handler_name in list(self.handlers.keys()):
                self.handlers[handler_name].tick()
        except KeyError: #means that no devices registered
            pass
    
    def _get_port(self):
        self.current_port += 1
        return self.current_port
    
    def close(self):
        for handler in  list(self.handlers.keys()):
            self.handlers[handler].close()
        self.vrc.close()
        self.mdns.close_browser()