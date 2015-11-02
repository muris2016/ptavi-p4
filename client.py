#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

if __name__ == "__main__":
    SERVER = (sys.argv[1])
    PORT = int(sys.argv[2])
    if sys.argv[3] == 'register':
        MSG = 'REGISTER sip:%s SIP/2.0\r\nExpires: %s\r\n\r\n' % (sys.argv[4],
                                                                  sys.argv[5])
    else:
        MSG = ' '.join(a for a in sys.argv[3:])

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((SERVER, PORT))

    print(MSG)
    my_socket.send(bytes(MSG, 'utf-8'))

    data = my_socket.recv(1024)

    print(data.decode('utf-8'))
    print("Finishing socket...")

    my_socket.close()
    print("End.")
