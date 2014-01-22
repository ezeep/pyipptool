pyipptool
=========

.. image::
   https://travis-ci.org/ezeep/pyipptool.png?branch=master
   :target: https://travis-ci.org/ezeep/pyipptool

.. image:: https://coveralls.io/repos/ezeep/pyipptool/badge.png
  :target: https://coveralls.io/r/ezeep/pyipptool


Convenient IPP request generator for python to interrogate CUPS or IPP devices, with the help of ipptool_.

.. _ipptool: http://www.cups.org/documentation.php/doc-1.7/man-ipptool.html

Setup
-----

.. code-block:: console

    python setup.py install


Tests
-----

.. code-block:: console

   python setup.py test

Configuration
-------------

Add the following content in  ``~/.pyipptool.cfg`` or ``/etc/pyipptool/pyipptol.cfg``.

.. code-block:: ini

    [main]
    ipptool_path = /usr/bin/ipptool
    ;If authentication is required
    login = admin
    password = secret
    graceful_shutdown_time = 2
    timeout = 10


Where ``ipptool_path`` points to the absolute path of your installed ipptool

Usage
-----

Create an infinite time subscription for printer-XYZ class for the ``rss`` notifier

.. code-block:: python

    >>> from pyipptool import create_printer_subscription
    >>> create_printer_subscription(
            printer_uri='http://localhost:631/classes/printer-XYZ',
            requesting_user_name='admin',
            notify_recipient_uri='rss://',
            notify_events='all',
            notify_lease_duration=0,
            notify_lease_expiration_time=0)
    23
