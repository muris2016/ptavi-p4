#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time

DATE_F = '%Y-%m-%d %H:%M:%S'


class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    client_dict = {}

    def clean_clients(self):
        """
        Clean's dictionary users with expired term
        """
        clean_list = [client for client in self.client_dict
                      if time.mktime(time.strptime(self.client_dict[client]
                                     ["expires"], DATE_F)) < time.time()]
        for client in clean_list:
            del self.client_dict[client]

    def register2json(self):
        """
        Print on a json file the client dict's information
        """
        with open('json_file.json', 'w') as outfile:
            json.dump(self.client_dict, outfile, sort_keys=True, indent=4)

    def json2register(self):
        """
        Get of json file information about clients, who made REGISTER method
        """
        try:
            with open('json_file.json', 'r') as outfile:
                json_str = outfile.read()
                self.client_dict = json.loads(json_str)
        except:
            pass

    def handle(self):
        """
        Recieve and arrange the request of REGISTER method
        """
        self.json2register()
        self.clean_clients()
        IP = self.client_address[0]
        PORT = self.client_address[1]
        print (IP, PORT, "wrote:")

        while 1:
            line = self.rfile.read().decode('utf-8').split()
            if not line:
                break
            print(" ".join(line))
            try:
                if 'REGISTER' in line:
                    address = line[1].split(':')[1]
                    expires = int(line[-1])
                    if expires != 0:
                        exp_t = expires + time.time()
                        exp_t = time.strftime(DATE_F, time.localtime(exp_t))
                        self.client_dict[address] = {'address': IP,
                                                     'expires': exp_t}
                    else:
                        del self.client_dict[address]
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                else:
                    self.wfile.write(b"SIP/2.0 400 BAD REQUEST\r\n\r\n")
            except:
                self.wfile.write(b"SIP/2.0 400 BAD REQUEST\r\n\r\n")
            self.register2json()

if __name__ == "__main__":
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
