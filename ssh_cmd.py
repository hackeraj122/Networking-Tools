'''
Acts as an SSH client.
Connects to an SSH server using credentials.
Executes a command on the server and retrieves the result.
Is useful for secure remote administration and automation.
'''

import paramiko                         # library is imported to handle the SSH connection.

def ssh_command(ip, port, user, passwd, cmd):       
    import paramiko

    try:
        client = paramiko.SSHClient()                                   # Create an SSH client object
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy)      # Automatically trust unknown servers (for first-time connections)
        client.connect(ip, port=port, username=user, password=passwd)   # Connect to the server using the provided details.

        _, stdout, stderr = client.exec_command(cmd)                    # Execute the command on the server.
        output = stdout.readlines() + stderr.readlines()                # Collect the command output and any error messages
        if output:
            print('---Output---')                                       # Print the output header.
            for line in output:                                         # Print each line of the output.
                print(line.strip())
    except paramiko.AuthenticationException:
        print("[ERROR] Authentication failed: Invalid username or password.")
    except paramiko.SSHException as ssh_error:
        print(f"[ERROR] SSH error occurred: {ssh_error}")
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
    finally:
        client.close()  # Ensure the connection is closed, even if an error occurs.

if __name__== '__main__':
    import getpass                                                     # Importing `getpass` to securely input passwords.
    # user = getpass.getuser()
    user = input('Username: ')
    password = getpass.getpass()                                        # Securely input the password without showing it on the screen
    
    ip = input("Enter server ip:") or "192.168.1.203"
    port = input("Enter port or <CR> :") or 2222
    cmd = input("Enter command or <CR>: ") or 'id'
    ssh_command(ip, port, user, password, cmd)




'''
Note: Before execution confirm that paramika is present and port 22 or any other port open or not and
      ssh server run in system (>>sudo service ssh start )

    Output:
─# python3 ssh_cmd.py
Username: kali
Password: 
Enter server ip:192.168.233.72
Enter port or <CR> :22
Enter command or <CR>: id
---Output---
uid=1000(kali) gid=1000(kali) groups=1000(kali),4(adm),20(dialout),24(cdrom),25(floppy),27(sudo),29(audio),30(dip),44(video),
46(plugdev),100(users),101(netdev),107(bluetooth),111(scanner),118(kaboxer),119(wireshark)

'''
