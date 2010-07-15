#!/usr/bin/env python
# encoding: utf-8
from setuptools import setup

setup(name='herald',
      version='0.4',
      description='Mobile Notifications for Transmission or uTorrent Downloads',
      author='Micah Ransdell',
      author_email='mjr578@gmail.com',
      url='http://github.com/micahr/herald/',
      packages=['herald'],
      scripts=['bin/notify.py'],
      install_requires=['notifo>=0.2.1','transmissionrpc>=0.5.0','uTorrent.Py>=0.1.1'],
      license='BSD-new',
      classifiers = (
                "Development Status :: 4 - Beta",
		        "License :: OSI Approved :: BSD License",
		        "Programming Language :: Python",
		        "Programming Language :: Python :: 2.5",
		        "Programming Language :: Python :: 2.6",
      )
     )