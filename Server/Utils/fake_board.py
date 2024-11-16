from zeroconf import Zeroconf, ServiceInfo
import socket

# Define the service details
service_type = "_haptics._udp.local."  # Updated to end with ._udp.local.
service_name = "vest_f._haptics._udp.local."
service_port = 12345  # Replace with the actual port number
service_ip = "127.0.0.1"  # Replace with the actual IP address

# Create the service info
info = ServiceInfo(
    service_type,
    service_name,
    addresses=[socket.inet_aton(service_ip)],
    port=service_port,
    properties={},
    server="vest_b.local."
)

# Initialize Zeroconf and register the service
zeroconf = Zeroconf()
zeroconf.register_service(info)

try:
    print(f"Service {service_name} of type {service_type} is now advertised.")
    input("Press enter to exit...\n\n")
finally:
    zeroconf.unregister_service(info)
    zeroconf.close()

