#!/usr/bin/env python
# encoding: utf-8
from distutils.core import setup

setup(name='trans-notify',
      version='0.3',
      description='Mobile Notifications for Transmission or uTorrent Downloads',
      author='Micah Ransdell',
      author_email='mjr578@gmail.com',
      url='http://github.com/micahr/trans-notify/',
      scripts=['trans-notify/notify.py'],
      requires=['notifo (>=0.2.1)','transmissionrpc (>=0.5.0)','uTorrent.Py (>=0.1.1)'],
      license='BSD-new',
      classifiers = (
                "Development Status :: 3 - Alpha",
		        "License :: OSI Approved :: BSD License",
		        "Programming Language :: Python",
		        "Programming Language :: Python :: 2.5",
		        "Programming Language :: Python :: 2.6",
      )
     )