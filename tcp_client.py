''' 
This is a simple TCP client script in Python that connects to a server running on 127.0.0.1 (localhost) at port 9998. The script performs the following tasks:
'''

import socket

target_host = "127.0.0.1"  # Server's IP address
target_port = 9998         # Must match the server's port

# Create a socket and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((target_host, target_port))

# Send a message to the server
client.send(b"Hello, Server! hii brother dfjkglgjldj")

# Receive the server's response
response = client.recv(4096)
print(f"Server response: {response.decode('utf-8')}")

# Close the connection
client.close()
