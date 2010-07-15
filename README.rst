============
herald
============

Introduction
=============
Herald is a python daemon for monitoring your Transmission_ or uTorrent_ downloads

Installation
=============
Install::

    python setup.py install


Usage
======
Start Herald from the command line::

    #: notify.py [options] -a start -l URL -n NOTIFO_USERNAME -k NOTIFO_KEY -c CLIENT [-o PORT -u CLIENT_USERNAME -p CLIENT_PASSWORD]

Stop Herald from the command line::

    #: notify.py [options] -a stop

Full Usage::

    Usage: notify.py [options]

    Options:
      -h, --help            show this help message and exit
      -a ACTION, --action=ACTION
                            Action to perform: start or stop [default: stop]
      -l URL, --url=URL     URL for Client
      -n NOTIFOUSER, --notifouser=NOTIFOUSER
                            Username for Notifo login
      -k NOTIFOKEY, --notifokey=NOTIFOKEY
                            Key for Notifo login
      -o PORT, --port=PORT  Port number for client login
      -u CLIENTUSER, --clientuser=CLIENTUSER
                            Username for client login
      -p PASSWORD, --password=PASSWORD
                            Password for client login
      -c CLIENT, --client=CLIENT
                            Choose which client to use: transmission or utorrent
                            [default: transmission]
      -d, --debug           Disable daemon and other production level functions

Requirements
======
herald requires an account on Notifo_ and Transmission_ or uTorrent_ installed on your machine.
You will also need the web interface turned on in order for everything to work. You can
access the web interface option in the Preferences -> Web tab.

Set either the Transmission or uTorrent settings based on which client you are using.


The NOTIFO_KEY can be found on your `Notifo Settings`_ page.

.. _Transmission: http://www.transmissionbt.com
.. _Notifo: http://notifo.com
.. _`Notifo Settings`: http://notifo.com/user/settings
.. _uTorrent: http://www.utorrent.com/