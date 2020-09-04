# dumb-server-monitor

This is a very barebones server uptime monitoring system.  Its original design purpose is to keep tabs on a Beowulf cluster from another location.

There are two components:

## Client (monitored)

The client machines run a cron job at desired intervals to "ping" the server(s) and let it know they're still alive.

NOTE: you must not have `PrivateNetwork=yes` in your systemd configs for cron, or this process will fail.

## Server (monitoring)

The server runs a Python-based webserver in order to accept "pings" from the clients.  The server maintains a list of currently known clients and can 
output them in either over the internet or into a file on request.

The server by default runs on port 55435.

# Guarantee of quality

I use this on both a 14-node cluster computer and a 20-node LAN, so if you can come
up with an improvement that helps both of us I'll implement it.  As is, the codebase
is *exactly* 300 lines of Python, so naturally I can't change that.
