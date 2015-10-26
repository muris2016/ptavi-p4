#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    client_dicc = {}

    def clean_clients(self):
        clean_list = []
        for client in self.client_dicc:
            expiration = time.mktime(time.strptime(self.client_dicc[client]["expires"], '%Y-%m-%d %H:%M:%S'))
            if expiration < time.time():
                clean_list.append(client)
        for client in clean_list:
            del self.client_dicc[client]

    def register2json(self):
        with open('json_file.json', 'w') as outfile:
            json.dump(self.client_dicc, outfile, sort_keys=True, indent=4)

    def json2register(self):
        try:
            with open('json_file.json', 'r') as outfile:
                json_str = outfile.read()
                self.client_dicc = json.loads(json_str)
        except:
            pass

    def handle(self):
        IP = self.client_address[0]
        PORT = self.client_address[1]
        print (IP, PORT, "wrote:")

        while 1:
            line = self.rfile.read().decode('utf-8')
            if not line:
                break
            print(line)
            if 'REGISTER' in line:
                self.clean_clients()
                self.json2register()
                address = line.split()[1].split(':')[1]
                expires = int(line.split()[-1])
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                if expires != 0:
                    time_expire = expires + time.time()
                    self.client_dicc[address] = {'address': IP,
                                                 'expires': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time_expire))}
                else:
                    try:
                        del self.client_dicc[address]
                    except KeyError:
                        break
                self.register2json()

if __name__ == "__main__":
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
