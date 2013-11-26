pyipptool
=========
[![Build Status](https://magnum.travis-ci.com/ezeep/pyipptool.png?token=1cZ3Jy2DStcoTAvezSS8)](https://magnum.travis-ci.com/ezeep/pyipptool#)

Convenient ipp request generator to interrogate CUPS or IPP devices

Setup
-----

python setup.py install

Tests
-----
python setup.py test

Configuration
-------------

Either in ```~/.pyipptool.cfg``` or in ```/etc/pyipptool/pyipptol.cfg```
add the following content

```config
[main]
ipptool_path = /usr/bin/ipptool
```

With the path to your installed ipptool

Usage
-----

Create infinite subscription for classes PUBLIC-PDF to ```rss``` notifier

```python
>>> from pyipptool import create_printer_subscription
>>> create_printer_subscription(
    printer_uri='http://localhost:631/classes/PUBLIC-PDF',
    requesting_user_name='admin',
    notify_recipient_uri='rss://',
    notify_events='all',
    notify_lease_duration=0,
    notify_lease_expiration_time=0)
23
```
