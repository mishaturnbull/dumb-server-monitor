# dumb-server-monitor

This is a very barebones server uptime monitoring system.  Its original design purpose is to keep tabs on a Beowulf cluster from another location.

There are two components:

## Client (monitored)

The client machines run a cron job at desired intervals to "ping" the server and let it know they're still alive.

## Server (monitoring)

The server runs a Python-based webserver in order to accept "pings" from the clients.  The server maintains a list of currently known clients and can 
output them in JSON format either over the internet or into a file on request.

The server by default runs on port 55435.
