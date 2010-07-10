#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import signal
import datetime
import time
import notifo
try:
    import transmissionrpc
    TRANSMISSION = True
except ImportError:
    TRANSMISSION = False
import daemon
try:
    from uTorrent import uTorrent
    UTORRENT = True
except ImportError:
    UTORRENT = False

from optparse import OptionParser

# Change these values to match your setup
if TRANSMISSION:
    TRANSMISSION_USER = 'admin'
    TRANSMISSION_PASSWORD = ''
    TRANSMISSION_URL = 'localhost'
    TRANSMISSION_PORT = 9091
if UTORRENT:
    UTORRENT_USER = 'admin'
    UTORRENT_PASSWORD = ''
    UTORRENT_URL = 'localhost'
    UTORRENT_PORT = 8080

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

def run_transmission(tc, notify):
    torrents = tc.list()
    
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

def run_utorrent(ut, notify, done_torrents):
    all_torrents = ut.webui_ls()
    for t in all_torrents:
        # location for logic with  utorrent files
        # add done torrents to done_torrents
        # every pass through check if newly done torrents are in done_torrents or not
        # if they are not, notify and add them
        pass

    return done_torrents


def startup():
    print 'Starting up Trans-Notify'
    if TRANSMISSION:
        try:
            tc = transmissionrpc.Client(TRANSMISSION_URL, port=TRANSMISSION_PORT,
                                user=TRANSMISSION_USER,
                                password=TRANSMISSION_PASSWORD)
        except transmissionrpc.transmission.TransmissionError:
            print 'Please set the location of Transmission and the proper username and password'
            sys.exit(1)
    if UTORRENT:
        ut = uTorrent(host=UTORRENT_URL, port=UTORRENT_PORT, username=UTORRENT_USER, password=UTORRENT_PASSWORD)
        
    daemon.daemonize(PID_FILE_LOCATION)
    notify = notifo.Notifo(NOTIFO_USER, NOTIFO_KEY)
    done_torrents = []
    while True:
        if TRANSMISSION:
            run_transmission(tc, notify)
        if UTORRENT:
            done_torrents = run_utorrent(ut, notify, done_torrents)
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


