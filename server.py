#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    client_dicc = {}
    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        IP = self.client_address[0]
        PORT = self.client_address[1]
        print (IP, PORT, "wrote:")

        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read().decode('utf-8')

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break
            print(line)
            
            if 'REGISTER' in line:
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                address = line.split()[1].split(':')[1]
                self.client_dicc[address] = IP
            # Si no hay más líneas salimos del bucle infinito

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    PORT = int(sys.argv[1])
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
