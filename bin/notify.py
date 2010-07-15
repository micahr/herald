#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import signal
import time
import daemon
from herald.Client import uTorrent, Transmission, ClientError

from optparse import OptionParser

# Don't bother changing this
PID_FILE_LOCATION =  '/tmp/trans-notify.pid'

def startup(options):
    if options.url is not None:
        client_options = [options.url,options.notifouser,
                        options.notifokey,options.port,
                        options.clientuser,options.password]
    else:
        print 'Please Specify a Url'
        sys.exit(1)
        
    try:
        if options.client == 'transmission':
            client = Transmission(*client_options)
        else:
            client = uTorrent(*client_options)
    except ClientError as e:
        print e.value
        sys.exit(1)

    if not options.debug:
        daemon.daemonize(PID_FILE_LOCATION)
    else:
        print 'Starting up Trans-Notify'

    while True:
        client.run()
        time.sleep(client.CHECK_INTERVAL)

def shutdown():
    try:
        pid = open(PID_FILE_LOCATION).read()
    except IOError:
        print 'Could not find PID file. Perhaps you already killed the process?'
        sys.exit(0)
    try:
        os.kill(int(pid), signal.SIGKILL)
    except OSError:
        print 'Trans-Notify is not currently running'
    os.remove(PID_FILE_LOCATION)
    print 'Killed Trans-Notify'

if __name__ == '__main__':
    usage = "usage: %prog [options]"

    parser = OptionParser(usage)
    parser.add_option('-a','--action',action="store", type="choice", default="stop", choices=['start','stop'],
                      dest="action", help="Action to perform: start or stop [default: %default]")
    parser.add_option('-l','--url', action="store", dest="url",
                      help="URL for Client")
    parser.add_option('-n','--notifouser', action="store", dest="notifouser",
                      help="Username for Notifo login")
    parser.add_option('-k','--notifokey', action="store", dest="notifokey",
                      help="Key for Notifo login")
    parser.add_option('-o','--port', action="store", type="int", dest="port",
                      help="Port number for client login")
    parser.add_option('-u','--clientuser', action="store", dest="clientuser",
                      help="Username for client login")
    parser.add_option('-p','--password', action="store", dest="password",
                      help="Password for client login")
    parser.add_option('-c','--client',
                      action="store", dest="client", type="choice", choices=['transmission','utorrent'],
                      default="transmission",
                      help="Choose which client to use: transmission or utorrent [default: %default]")
    parser.add_option('-d','--debug',
                      action="store_true", dest="debug", default=False,
                      help="Disable daemon and other production level functions")

    (options, args) = parser.parse_args()


    if options.action == 'start':
        startup(options)
    else:
        shutdown()


