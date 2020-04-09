#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This file is very simply meant to send the server the message necessary
to dump file output.  The server is assumed to be running on localhost.
"""

import socket
import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read('dsm-server.conf')

MESSAGE = "\x13\x1e_\x1e"


def main():
    port = int(CONFIG['network']['port'])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', port))
    sock.sendall(bytes(MESSAGE, 'utf-8'))


if __name__ == '__main__':
    main()
