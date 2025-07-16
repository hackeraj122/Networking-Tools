"""
This code creates a network proxy tool. It listens for connections on a local port, forwards traffic to a remote host, and can modify or 
inspect the data being sent or received.
"""

import sys                   #The sys module in Python provides access to system-specific parameters and functions that interact closely with the Python interpreter.
import socket
import threading

HEX_FILTER = ''.join([(len(repr(chr(i)))==3) and chr(i) or '.' for i in range (256)])

def hexdump(src, length=16, show=True):             # function that formats the received binary data into a human-readable hex dump for debugging purposes.
    if isinstance(src, bytes):                      
        src= src.decode()
    results = list()
    for i in range (0, len(src),length):            #Loop through the data in chunks of length (default: 16 bytes per line).
        word = str(src[i:i+length])                 #extracts a slice of src containing up to length characters.
        printable = word.translate(HEX_FILTER)      #HEX_FILTER maps non-printable characters to a period (.), ensuring only printable ASCII characters are displayed

        #Converts each character in word to its hexadecimal value using ord(c) and formats it as a 2-digit uppercase hex (02X)
        hexa = ' '.join([f'{ord(c):02X}' for c in word]) 
        hexwidth = length*3                                             #Format the Line
        results.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')

    if show:
        for line in results:
            print(line)
    else:
        return results
    

def recieve_from(connection):
    buffer = b""
    connection.settimeout(10)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    return buffer

def request_handler(buffer):
    #perform packets modifications
    return buffer

def response_handler(buffer):
    # perform packet modification
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, recive_first):       #function manage traffic direction between remote or local machine
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host,remote_port))                            #Used on the client-side to connect to a server's IP address and port.

    if recive_first:
        remote_buffer = recieve_from(remote_socket)                  #data come from remote host put into remote_buffer variable
        hexdump(remote_buffer)                                       #function formats the received binary data into a human-readable hex dump for debugging purposes.

    remote_buffer = response_handler(remote_buffer)                 #function is called to modify or inspect the data received from the remote server.
    if len(remote_buffer):
        print("[<==] Sending %d byte to localhost." % len(remote_buffer))
        client_socket.send(remote_buffer)

    while True:
        local_buffer = recieve_from(client_socket)              #data come from 
        if len(local_buffer):
            line = "[==>]Recieved %d bytes from localhost." % len(remote_buffer)
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==> ] Sent to remote.")
        
        remote_buffer = recieve_from(remote_socket)
        if len(remote_buffer):
            print("[<==] Recived %d bytes from remote, " % len(remote_buffer))
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")
        
        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data . Closing the connection.")
            break


def server_loop(local_host, local_port, remote_host, remote_port, recieve_first):
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)                           #create object for TCP client socket
    try:
        server.bind((local_host,local_port))                                           #Used on the server-side to specify where it will listen for incoming connections.
    except Exception as e:
        print("problem on bind : %r" % e)
        print("[!!] Failed to listen on %s:%d" %(local_host, local_port))
        print("[!!] Check for other listening socket or correct permission .")
        sys.exit(0)
    
    print("[*] Listening on %s:%d " %(local_host,local_port))
    server.listen(5)                                                                #5 client listen at a time
    while True:
        client_socket, addr = server.accept()                                       # store information related to client i.e ip and port
        
        #print out the local connection information
        line = "> Recieving incoming connection from %s:%d " %(addr[0],addr[1])
        print(line)

        #start a thread to talk the remote host
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port, recieve_first)) #each client do operation in proxy handler function
        proxy_thread.start()                                                                                                    #with providing all arguments

def main():
    if len(sys.argv[1:]) != 5:                                              # it is a list that stores command-line arguments passed to the script
        print("Usage: ./proxy.py [localhost] [localport]", end='')
        print("[remotehost] [remoteport] [recieve_first]")
        print("Example : ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)
    local_host = sys.argv[1]                        # assign argument values into specified variable
    local_port = int(sys.argv[2])
    remote_host= sys.argv[3]
    remote_port = int(sys.argv[4])
    recieve_first = sys.argv[5]
    if "True" in recieve_first:
        recieve_first = True
    else:
        recieve_first = False
    
    server_loop(local_host,local_port, remote_host, remote_port, recieve_first)

if __name__ == '__main__':
    main()
