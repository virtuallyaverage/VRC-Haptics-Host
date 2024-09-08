from zeroconf import ServiceBrowser, Zeroconf, ServiceListener

class MyListener(ServiceListener):
    def add_service(self, zeroconf, type, name):
        print(f"Service {name} added, type: {type}")

    def remove_service(self, zeroconf, type, name):
        print(f"Service {name} removed, type: {type}")
        
    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated, type: {type_}")

if __name__ == "__main__":

    zeroconf = Zeroconf()
    listener = MyListener()
    
    # Browsing for all services
    browser = ServiceBrowser(zeroconf, "_haptics._osc.local.", listener)
    
    try:
        input("Press enter to exit...\n\n")
    finally:
        zeroconf.close()
