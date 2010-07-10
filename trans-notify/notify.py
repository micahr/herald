#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import signal
import datetime
import time
import notifo
import daemon
try:
    import transmissionrpc
except ImportError:
    print 'No TransmissionRPC Library'
try:
    from uTorrent import uTorrent
except ImportError:
    print 'No uTorrent.py Library'

from optparse import OptionParser

# Change these values to match your setup
TRANSMISSION_USER = 'admin'
TRANSMISSION_PASSWORD = ''
TRANSMISSION_URL = 'localhost'
TRANSMISSION_PORT = 9091

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

def run_utorrent(ut, notify, done_torrents, seen_torrents):
    # Looking for all torrents that haven't previously been marked as done
    unfinished_torrents = [x for x in ut.webui_ls() if x not in done_torrents]
    # Looking for all torrents that are neither done, or been recorded previously
    unseen_torrents = [x for x in ut.webui_ls() if x not in seen_torrents or done_torrents]
    for torrent in unfinished_torrents:
        if float(torrent[uTorrent.UT_TORRENT_STAT_P1000_DONE]) / 10 == 100.0:
            notify.send_notification(to=NOTIFO_USER,
                                     msg='Your download: %s is finished' % torrent[uTorrent.UT_TORRENT_PROP_NAME],
                                     label=NOTIFO_LABEL,
                                     title=NOTIFO_TRANS_FINISHED)
            done_torrents.append(torrent)
            # removing a torrent that is now done from the seen_torrents so it doesn't grow infinitely large
            if torrent in seen_torrents:
                seen_torrents.remove(torrent)

    for torrent in unseen_torrents:
        notify.send_notification(to=NOTIFO_USER,
                                     msg='Your download: %s has started' % torrent[uTorrent.UT_TORRENT_PROP_NAME],
                                     label=NOTIFO_LABEL,
                                     title=NOTIFO_TRANS_STARTED)
        seen_torrents.append(torrent)

    return (done_torrents, seen_torrents)


def startup(enable_daemon, client):
    if client == 'transmission':
        try:
            tc = transmissionrpc.Client(TRANSMISSION_URL, port=TRANSMISSION_PORT,
                                user=TRANSMISSION_USER, password=TRANSMISSION_PASSWORD)
        except transmissionrpc.transmission.TransmissionError:
            print 'Please set the location of Transmission and the proper username and password'
            sys.exit(1)
    else:
        ut = uTorrent.uTorrent(host=UTORRENT_URL, port=UTORRENT_PORT,
                               username=UTORRENT_USER, password=UTORRENT_PASSWORD)

    print 'Starting up Trans-Notify'
    if not enable_daemon:
        daemon.daemonize(PID_FILE_LOCATION)
    notify = notifo.Notifo(NOTIFO_USER, NOTIFO_KEY)
    done_torrents, seen_torrents = [], []
    while True:
        if client == 'transmission':
            run_transmission(tc, notify)
        else:
            done_torrents, seen_torrents = run_utorrent(ut, notify, done_torrents, seen_torrents)
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
    usage = "usage: %prog [options] start|stop"

    parser = OptionParser(usage)
    parser.add_option('-d','--debug',
                      action="store_true", dest="debug", default=False,
                      help="Disable daemon and other production level functions")
    parser.add_option('-c','--client',
                      action="store", dest="client", default="transmission",
                      help="Choose which client to use: transmission or utorrent [default: %default]")
    
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("No action specified")
    else:
        if args[0].lower() == 'start':
            startup(options.debug, options.client)
        else:
            shutdown()


