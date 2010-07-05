============
trans-notify
============

Introduction
=============
trans-notify is a python daemon for monitoring your Transmission_ downloads

Installation
=============
Install::

    python setup.py install


Usage
======
run notify.py from the command line::

    #: notify.py


Requirements
======
trans-notify requires an account on Notifo_ and Transmission_ installed on your machine.
You will also need the web interface turned on in order for everything to work. You can
access the web interface option in the Preferences -> Web tab

You will need to change a few settings in notify.py before install::

    TRANSMISSION_USER = 'admin'
    TRANSMISSION_PASSWORD = ''
    TRANSMISSION_URL = 'localhost'
    TRANSMISSION_PORT = 9091
    NOTIFO_USER = '[Personal Notifo.com Username]'
    NOTIFO_KEY = '[Personal Notifo.com Key]'

The NOTIFO_KEY can be found on your `Notifo Settings`_ page.

.. _Transmission: http://www.transmissionbt.com
.. _Notifo: http://notifo.com
.. _`Notifo Settings`: http://notifo.com/user/settings