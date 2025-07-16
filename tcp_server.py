'''
This is a multi-threaded TCP server that listens for incoming client connections on port 9998. It can handle multiple clients simultaneously by using threads.
'''
import socket
import threading

IP = '0.0.0.0'  # Listen on all interfaces
PORT = 9998     # Port for the server

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))                 #IP and PORT we want to listen
    server.listen(2)                        # at a time listening clients
    print('[*] Listening on %s:%d' %(IP,PORT))
    while True:
        client, address = server.accept()       # store information related to client i.e ip and port
        print('[*] Accepted connection from %s:%d' %(address[0],address[1]))
        client_handler = threading.Thread(target=handle_client, args=(client,))     # use to create seperate connection to each client 
        client_handler.start()

def handle_client(client_socket):                           # perform whatever the operation with client 
    
    request = client_socket.recv(1024)
    print('[*] Received:%s' %(request.decode("utf-8")))
    client_socket.send(b'ACK')  # Send acknowledgment

if __name__ == '__main__':
    main()
  
