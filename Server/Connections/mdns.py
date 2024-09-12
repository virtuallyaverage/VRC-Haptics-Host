from zeroconf import ServiceBrowser, Zeroconf, ServiceListener
from psutil import net_if_addrs

class MDNSHandler():
    def __init__(self) -> None:
        self.detected_devices = {}
        
        self._zeroconfig = Zeroconf()
        self._handler = _MDNSListener(self)
        self._browser = ServiceBrowser(self._zeroconfig, "_haptics._osc.local.", self._handler)
        
        self._callbacks = []
        
    def subscribe(self, callback_func: callable):
        """Subscribes to device updates. 

        Args:
            callback_func (callable): callback function
        """
        self._callbacks.append(callback_func)
    
    def _on_device_added(self, info) -> None:
        name = info.server.split('.')[0]
        new_device = {
            'ip': info.addresses[0],
            'port': 1027,
            'name': info.name
        }
        
        # keyed by split of server name: e.g: vest.local -> vest
        self.detected_devices[name] = new_device
        
        for callback in self._callbacks:
            callback(name,  new_device)
     
    def close_browser(self) -> None:
        self._zeroconfig.close()
    
    
# Service: vest._haptics._osc.local. info: ServiceInfo(type='_haptics._osc.local.', name='vest._haptics._osc.local.', addresses=[b'\xc0\xa8\x01d'], port=1027, weight=0, priority=0, server='vest.local.', properties={b'': None}, interface_index=None)
                                                                                                                                            #ip as raw values
class _MDNSListener(ServiceListener):
    """Listener class for internal use by the MDNSHandler

    Args:
        ServiceListener (callback): callback for the zeroconf ServiceBrowser
    """
    def __init__(self, handler: MDNSHandler) -> None:
        self.found_services = []  # List to store found services
        self.handler = handler
        super().__init__()
        
    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        if info:
            self.found_services.append(info)  # Add service info to the list
            self.handler._on_device_added(info)

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")
        
    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated, type: {type_}")

if __name__ == "__main__":
    # Start the main handler
    dns_handler = MDNSHandler()
    
    #whait till one of our haptics services shows up
    while dns_handler.get_possible() == []:
        pass        
        

    deviceInfo = dns_handler.get_possible()
    print(deviceInfo)

