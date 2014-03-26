pyipptool
=========

.. image::
   https://travis-ci.org/ezeep/pyipptool.svg?branch=master
   :target: https://travis-ci.org/ezeep/pyipptool

.. image:: https://coveralls.io/repos/ezeep/pyipptool/badge.png
  :target: https://coveralls.io/r/ezeep/pyipptool

.. image:: https://pypip.in/v/pyipptool/badge.png
   :target: https://crate.io/packages/pyipptool/
   :alt: Latest PyPI version

.. image:: https://landscape.io/github/ezeep/pyipptool/master/landscape.png
   :target: https://landscape.io/github/ezeep/pyipptool/master
   :alt: Code Health


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
    cups_uri = http://localhost:631/
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
            notify_lease_duration=0)
    {'Name': 'Create Printer Subscription',
     'Operation': 'Create-Printer-Subscription',
     'RequestAttributes': [{'attributes-charset': 'utf-8',
                            'attributes-natural-language': 'en',
                            'printer-uri': 'http://localhost:631/classes/printer-XYZ',
                            'requesting-user-name': 'admin'},
                           {'notify-events': 'all',
                            'notify-lease-duration': 0,
                            'notify-recipient-uri': 'rss://'}],
     'ResponseAttributes': [{'attributes-charset': 'utf-8',
                             'attributes-natural-language': 'en'},
                            {'notify-subscription-id': 23}],
     'StatusCode': 'successful-ok',
     'Successful': True,
     'notify-subscription-id': 23}
