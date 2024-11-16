from pythonosc import udp_client

# Set up the client with the target IP and port
client = udp_client.SimpleUDPClient("127.0.0.1", 9001)

prefix = "/avatar/parameters/h"
group = input("Group?: ")
last_motor = 0

while True:
    motor_num = input(f"{group}_M#: ")
    
    client.send_message(f"{prefix}/{group}_{last_motor}", 0.0)
    client.send_message(f"{prefix}/{group}_{motor_num}", 0.9)
    addr = f"{prefix}/{group}_{motor_num}"
    print(f"Sent: {addr}")
    last_motor = motor_num
    
    if (motor_num == 's'):
        for i in range(35):
            client.send_message(f"{prefix}/{group}_{i}", 0.0)
            
        quit()
        

