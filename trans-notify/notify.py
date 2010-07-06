#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import signal
import datetime
import time
import notifo
import transmissionrpc
import daemon
from optparse import OptionParser

# Change these values to match your setup
TRANSMISSION_USER = 'admin'
TRANSMISSION_PASSWORD = ''
TRANSMISSION_URL = 'localhost'
TRANSMISSION_PORT = 9091
NOTIFO_USER = '[Personal Notifo.com Username]'
NOTIFO_KEY = '[Personal Notifo.com Key]'

# Time in seconds between checking for changes
# Change this if you would like to poll less or more frequently
CHECK_INTERVAL = 30

# Feel free to change these values if you want a different notice on your Phone
NOTIFO_LABEL = 'TRANS-NOTIFY'
NOTIFO_TRANS_FINISHED = 'Download Finished'
NOTIFO_TRANS_STARTED = 'Download Started'

# Don't bother with this one
PID_FILE_LOCATION =  '/tmp/trans-notify.pid'


DELTA = datetime.timedelta(seconds=CHECK_INTERVAL)

def run(tc):
    torrents = tc.list()
    notify = notifo.Notifo(NOTIFO_USER, NOTIFO_KEY)

    for torrent in torrents.values():
        detailed = tc.info(torrent.id)[torrent.id]
        if detailed.date_done >= datetime.datetime.now() - DELTA:
            notify.send_notification(to=NOTIFO_USER,
                                     msg='Your download: %s is finished' % detailed.name,
                                     label=NOTIFO_LABEL,
                                     title=NOTIFO_TRANS_FINISHED)

        if detailed.date_added >= datetime.datetime.now() - DELTA:
            notify.send_notification(to=NOTIFO_USER,
                                     msg='Your download: %s has started' % detailed.name,
                                     label=NOTIFO_LABEL,
                                     title=NOTIFO_TRANS_STARTED)

def startup():
    print 'Starting up Trans-Notify'
    try:
        tc = transmissionrpc.Client(TRANSMISSION_URL, port=TRANSMISSION_PORT,
                                user=TRANSMISSION_USER,
                                password=TRANSMISSION_PASSWORD)
    except transmissionrpc.transmission.TransmissionError:
        print 'Please set the location of Transmission and the proper username and password'
        sys.exit(1)
    daemon.daemonize(PID_FILE_LOCATION)
    while True:
        run(tc)
        time.sleep(CHECK_INTERVAL)

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
    usage = "usage: %prog start|stop"

    parser = OptionParser(usage)
    
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("No action specified")
    else:
        if args[0].lower() == 'start':
            startup()
        else:
            shutdown()


