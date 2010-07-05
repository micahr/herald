#!/usr/bin/env python
# encoding: utf-8
import transmissionrpc
import datetime
import time
import notifo
import daemon

# Change these values to match your setup
TRANSMISSION_USER = 'admin'
TRANSMISSION_PASSWORD = ''
TRANSMISSION_URL = 'localhost'
TRANSMISSION_PORT = 9091

NOTIFO_USER = '[Personal Notifo.com Username]'
NOTIFO_KEY = '[Personal Notifo.com Key]'
NOTIFO_LABEL = 'TRANS-NOTIFY'
NOTIFO_TRANS_FINISHED = 'Download Finished'
NOTIFO_TRANS_STARTED = 'Download Started'

# Time in seconds between checking for changes
CHECK_INTERVAL = 30
DELTA = datetime.timedelta(seconds=CHECK_INTERVAL)

def run():
    tc = transmissionrpc.Client(TRANSMISSION_URL, port=TRANSMISSION_PORT,
                                user=TRANSMISSION_USER,
                                password=TRANSMISSION_PASSWORD)

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

if __name__ == '__main__':
    daemon.daemonize('/tmp/trans-notify.pid')
    while True:
        run()
        time.sleep(CHECK_INTERVAL)
