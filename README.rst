============
trans-notify
============

Introduction
=============
trans-notify is a python daemon for monitoring your Transmission_ or uTorrent_ downloads

Installation
=============
Install::

    python setup.py install


Usage
======
Start Trans-Notify from the command line::

    #: notify.py [options] start

Stop Trans-Notify from the command line::

    #: notify.py [options] stop

Full Usage::

    Usage: notify.py [options] start|stop

    Options:
      -h, --help            show this help message and exit
      -d, --debug           Disable daemon and other production level functions
      -c CLIENT, --client=CLIENT
                        Choose which client to use: transmission or utorrent
                        [default: transmission]

Requirements
======
trans-notify requires an account on Notifo_ and Transmission_ or uTorrent_ installed on your machine.
You will also need the web interface turned on in order for everything to work. You can
access the web interface option in the Preferences -> Web tab.

Set either the Transmission or uTorrent settings based on which client you are using.

You will need to change a few settings in notify.py before install::

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

The NOTIFO_KEY can be found on your `Notifo Settings`_ page.

.. _Transmission: http://www.transmissionbt.com
.. _Notifo: http://notifo.com
.. _`Notifo Settings`: http://notifo.com/user/settings
.. _uTorrent: http://www.utorrent.com/