import os 
import paramiko
import socket
import sys
import threading

import paramiko.transport

CWD = os.path.dirname(os.path.realpath(__file__))
#HOSTKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa_key'))
HOSTKEY = paramiko.RSAKey(filename='/home/kali/keys/test_rsa_key')


class Server (paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_chennel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_auth_password(self, username, password):
        if (username == 'tim') and (password == 'sekret'):
            return paramiko.AUTH_SUCCESSFUL


if __name__ == '__main__':
    server = '192.168.233.72'
    ssh_port = 2222
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, ssh_port))
        sock.listen(100)
        print('[+] Listening for connection ....')
        client, addr = sock.accept()
    except Exception as e :
        print('[-] Listen failed :'+ str(e))
        sys.exit(1)
    else:
         print('[+] GOt a connection ', client, addr)
    
    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSTKEY)
    server = Server()
    bhSession.start_server(server=server)

    chan = bhSession.accept(20)
    if chan is None:
        print('**** No channel')
        sys.exit(1)
    
    print('[+] Authenticated !')
    print(chan.recv(1024))
    chan.send('Welcome to bh__ssh')
    try:
        while True:
            command = input('Enter command :')
            if command != 'exit':
                chan.send(command)
                r = chan.recv(8192)
                print(r.decode())

            else:
                chan.send('exit')
                print('exiting')
                bhSession.close()
                break
    except KeyboardInterrupt :
        bhSession.close()
