#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This is the server side of dumb-server-manager.  It's responsible for the
monitoring and keeping-track-of clients who "ping" us occasionally.
"""

import configparser
import socketserver
from datetime import datetime
import functools
import time

CONFIG = configparser.ConfigParser()
CONFIG.read("dsm-server.conf")

@functools.lru_cache(maxsize=16)
def cbool(value):
    """
    Short for "config bool".  Determines whether or not a config value
    should be True or False based on the [meta] section.
    :param value: value in question
    :return: True or False
    """
    truthy = CONFIG['meta']['accepted-true'].split(' ')
    falsy = CONFIG['meta']['accepted-false'].split(' ')
    default = bool(CONFIG['meta']['default'].capitalize())
    if value in truthy:
        return True
    elif value in falsy:
        return False
    else:
        return default

class Client(object):
    """
    This is the object that the server uses to represent a client it's
    monitoring.
    """

    def __init__(self, name,
                 last_seen_time=None,
                 ):
        self.name = name
        self.last_seen_time = last_seen_time or datetime.now()

    def seen_again(self):
        """
        Updates the client.  Call this when the client contacts us
        successfully.
        :return: nothing
        """
        self.last_seen_time = datetime.now()

    def is_in_list(self, clients):
        """
        Check our name against a record of other clients.
        :param clients: List[Client].
        :return: index of client if in list, else False.
        """
        i = 0
        for client in clients:
            if client.name == self.name:
                return i
            i += 1
        return False

    def repr_for_file(self):
        """
        Get a string representation of this Client object to be put in a file.
        :return: One line string.
        """
        return "{}\t{}".format(
            self.name,
            self.last_seen_time.strftime("%Y-%m-%d %H:%M:%S")
        )

    def repr_for_network(self):
        """
        Get a string representation of the Client object to be put in
        the network.
        :return: ASCII string terminated by 0x09 (tab).
        """
        return "{}\x1d{}\t".format(
            self.name,
            self.last_seen_time.strftime("%Y%m%d%H%M%S")
        )


class Server(socketserver.BaseRequestHandler):
    """
    This is the actual server itself.
    """

    def setup(self):
        self.clients = []

        if CONFIG["security"]["psk"].strip():
            self.password_hash = CONFIG['security']['psk'].strip()
        else:
            self.password_hash = None

        if cbool(CONFIG["security"]["allow-file-output"]):
            self.file_dest = CONFIG["security"]["file-output-dest"]
        else:
            self.file_dest = None

        self.allow_network_output = \
            cbool(CONFIG['security']['allow-network-output'])

    def update_client(self, cname):
        newclient = Client(cname)
        is_in_list = newclient.is_in_list(self.clients)
        if not is_in_list:
            # add client to the list
            self.clients.append(newclient)
        else:
            # update existing client
            self.clients[is_in_list].seen_again()

    def handle_client_update(self, cname, passhash):
        cname = cname.strip()
        passhash = passhash.strip()

        if self.password_hash:
            if passhash != self.password_hash:
                # got password wrong, just forget about them
                return

        self.update_client(cname)

    def handle_network_output(self):
        if not self.allow_network_output:
            return  # nope!

        message = ""
        for client in self.clients:
            message += client.repr_for_network()

        send = bytes(message, 'utf-8')
        self.request.sendall(send)

    def handle_file_output(self):
        if not self.file_dest:
            return  # nope!

        lines = []
        for client in self.clients:
            lines.append(client.repr_for_file())

        with open(self.file_dest, 'w') as outputfile:
            outputfile.writelines(lines)

    def handle(self):
        # This has to be in a loop
        while True:
            self.data = self.request.recv(1024).strip()
            if not self.data:
                # client disconnected
                break

            flag, cname, passhash = self.data.split('\x1e')

            if flag == '\x11':
                self.handle_client_update(cname, passhash)
            elif flag == '\x12':
                self.handle_network_output()
            elif flag == '\x13':
                self.handle_file_output()

    def finish(self):
        # not much to do here
        pass

if __name__ == '__main__':
    port = int(CONFIG['network']['port'])
    host = CONFIG['network']['address'].strip()
    allow_rebind = cbool(CONFIG['network']['allow-rebind'])

    server = socketserver.TCPServer((host, port), Server)
    if allow_rebind:
        server.allow_reuse_address = True
    server.serve_forever()
