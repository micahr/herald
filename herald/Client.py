# encoding: utf-8
import datetime
import notifo

class ClientError(Exception):
    pass

class Client(object):
    """Base Class for clients"""

    # Feel free to change these values if you want a different notice on your Phone
    NOTIFO_LABEL = 'HERALD'
    NOTIFO_FINISHED = 'Download Finished'
    NOTIFO_STARTED = 'Download Started'

    # Time in seconds between checking for changes
    # Change this if you would like to poll less or more frequently
    CHECK_INTERVAL = 30
    DELTA = datetime.timedelta(seconds=CHECK_INTERVAL)

    def __init__(self, url, notifo_username, notifo_key, port=None, username=None, password=None):
        self.URL = url
        self.NOTIFO_USERNAME = notifo_username
        self.NOTIFO_KEY = notifo_key
        self.PORT = port
        self.USERNAME = username
        self.PASSWORD = password
        self.notifo = notifo.Notifo(self.NOTIFO_USERNAME, self.NOTIFO_KEY)

    def get_torrents(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

    def send_finished_notification(self, torrent_name):
        self.notifo.send_notification(to=self.NOTIFO_USERNAME,
                                         msg='Your download: %s is finished' % torrent_name,
                                         label=self.NOTIFO_LABEL,
                                         title=self.NOTIFO_FINISHED)

    def send_started_notification(self, torrent_name):
        self.notifo.send_notification(to=self.NOTIFO_USERNAME,
                                         msg='Your download: %s has started' % torrent_name,
                                         label=self.NOTIFO_LABEL,
                                         title=self.NOTIFO_STARTED)


class uTorrent(Client):
    try:
        from uTorrent import uTorrent as ut
    except ImportError:
        print 'No uTorrent.py Library'

    def __init__(self, *args, **kwargs):
        super(uTorrent, self).__init__(*args, **kwargs)
        try:
            self.client = self.ut.uTorrent(host=self.URL, port=self.PORT,
                                username=self.USERNAME, password=self.PASSWORD)
        except:
            raise ClientError('Please set the location of uTorrent and the proper username and password')
        
        self.done_torrents, self.seen_torrents = [],[]

    def get_torrents(self):
        return self.client.webui_ls()
        return self.client

    def run(self):
        # Looking for all torrents that haven't previously been marked as done
        unfinished_torrents = [x for x in self.get_torrents() if x[self.ut.UT_TORRENT_PROP_NAME] not in self.done_torrents]
        # Looking for all torrents that are neither done, or been recorded previously
        unseen_torrents = [x[self.ut.UT_TORRENT_PROP_NAME] for x in self.get_torrents()
                           if x[self.ut.UT_TORRENT_PROP_NAME] not in self.seen_torrents
                            and x[self.ut.UT_TORRENT_PROP_NAME] not in self.done_torrents]
        for torrent in unfinished_torrents:
            if float(torrent[self.ut.UT_TORRENT_STAT_P1000_DONE]) / 10 == 100.0:
                self.send_finished_notification(torrent[self.ut.UT_TORRENT_PROP_NAME])
                # removing a torrent that is now done from the seen_torrents so it doesn't grow infinitely large
                self.done_torrents.append(torrent[self.ut.UT_TORRENT_PROP_NAME])
                self.seen_torrents.remove(torrent[self.ut.UT_TORRENT_PROP_NAME])

        for torrent in unseen_torrents:
            self.send_started_notification(torrent[self.ut.UT_TORRENT_PROP_NAME])
            self.seen_torrents.append(torrent[self.ut.UT_TORRENT_PROP_NAME])



class Transmission(Client):
    try:
        import transmissionrpc as tran
    except ImportError:
        print 'No TransmissionRPC Library'

    def __init__(self, *args, **kwargs):
        super(Transmission, self).__init__(*args, **kwargs)
        try:
            self.client = self.tran.Client(self.URL, port=self.PORT, user=self.USERNAME, password=self.PASSWORD)
        except:
            raise ClientError('Please set the location of Transmission and the proper username and password')

    def get_torrents(self):
        return self.client.list()

    def run(self):
        for torrent in self.get_torrents().values():
            detailed = self.client.info(torrent.id)[torrent.id]
            if detailed.date_done >= datetime.datetime.now() - self.DELTA:
                self.send_finished_notification(detailed.name)
            if detailed.date_added >= datetime.datetime.now() - self.DELTA:
                self.send_started_notification(detailed.name)





        