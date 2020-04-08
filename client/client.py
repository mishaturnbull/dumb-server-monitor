#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This is the client side of dumb-server-monitor.  It's responsible for "pinging"
servers as defined in servers.conf and letting them know we're alive.
"""

import configparser
import socket
import hashlib

SERVERS = configparser.ConfigParser()
SERVERS.read('servers.conf')


class Server(object):
    """
    This is the object a client uses to represent a server.
    """

    def __init__(self, address, port, ourname, psk_hash):
        self.address = address
        self.port = port
        self.ourname = ourname
        self.psk_hash = psk_hash


def process_psk(server_id):
    """
    Goes and gets the PSK for a given server name.  Returns either a
    SHA256 hash, or None.
    :param server_id: server header name
    :return: None or 64-byte string.
    """


def get_server_list():
    servers = []
    for server in SERVERS:
        servers.append(Server(
            SERVERS[server]['address'],
            int(SERVERS[server]['port']),
            SERVERS[server]['ourname'],
            process_psk(server),
        ))
    return servers


def construct_message(server):
    """
    Gets an ASCII string to send off to a given server.
    :param server: Server object
    :return: string
    """
    return "\x11\x1e{}\x1e{}".format(
        server.ourname,
        server.psk_hash if server.psk_hash else ''
    )


def update_server(server):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server.address, server.port))
    sock.sendall(bytes(construct_message(server), 'utf-8'))


def main():
    servers = get_server_list()
    for server in servers:
        update_server(server)


if __name__ == '__main__':
    main()
