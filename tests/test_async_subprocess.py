import BaseHTTPServer
import os
import SocketServer
import socket
import threading
import time

from pkipplib import pkipplib
import pytest
import tornado.testing


TRAVIS_USER = os.getenv('TRAVIS_USER', 'travis')
TRAVIS_BUILD_DIR = os.getenv('TRAVIS_BUILD_DIR')


class AsyncSubprocessTestCase(tornado.testing.AsyncTestCase):

    ipptool_path = ('%s/ipptool-20130731/ipptool' % TRAVIS_BUILD_DIR if
                    TRAVIS_BUILD_DIR else '/usr/bin/ipptool')
    config = {'ipptool_path': ipptool_path,
              'login': TRAVIS_USER,
              'password': 'travis',
              'graceful_shutdown_time': 2,
              'timeout': 5}

    @tornado.testing.gen_test
    def test_async_call(self):
        from pyipptool.core import AsyncIPPToolWrapper
        from pyipptool.forms import get_subscriptions_form

        class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
            """
            HTTP Handler that will make ipptool waiting
            """
            protocol_version = 'HTTP/1.1'

            def do_POST(self):
                # return a real IPP Response thanks to pkipplib
                ipp_request = pkipplib.IPPRequest(
                    self.rfile.read(
                        int(self.headers.getheader('content-length'))))
                ipp_request.parse()
                try:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/ipp')
                    self.end_headers()
                    ipp_response = pkipplib.IPPRequest(
                        operation_id=pkipplib.IPP_OK,
                        request_id=ipp_request.request_id)
                    ipp_response.operation['attributes-charset'] =\
                        ('charset', 'utf-8')
                    ipp_response.operation['attributes-natural-language'] =\
                        ('naturalLanguage', 'en-us')
                    self.wfile.write(ipp_response.dump())
                finally:
                    assassin = threading.Thread(target=self.server.shutdown)
                    assassin.daemon = True
                    assassin.start()

        PORT = 6789
        while True:
            try:
                httpd = SocketServer.TCPServer(("", PORT), Handler)
            except socket.error as exe:
                if exe.errno in (48, 98):
                    PORT += 1
                else:
                    raise
            else:
                break
        httpd.allow_reuse_address = True

        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()

        wrapper = AsyncIPPToolWrapper(self.config, self.io_loop)
        wrapper.config['cups_uri'] = 'http://localhost:%s/' % PORT

        request = get_subscriptions_form.render(
            {'operation_attributes':
             {'printer_uri': 'http://localhost:%s/printers/fake' % PORT}}
        )

        response = yield wrapper._call_ipptool(request)
        for key in ('RequestId', 'ipptoolVersion', 'Version'):
            # May diverge depending of version of ipptool
            try:
                del response[key]
            except KeyError:
                pass
        expected_response = {'Name': 'Get Subscriptions',
                             'Operation': 'Get-Subscriptions',
                             'Successful': True,
                             'RequestAttributes':
                             [{'attributes-charset': 'utf-8',
                               'attributes-natural-language': 'en',
                               'printer-uri':
                               'http://localhost:%s/printers/fake' % PORT}],
                             'ResponseAttributes':
                             [{'attributes-charset': 'utf-8',
                               'attributes-natural-language': 'en-us'}],
                             'StatusCode': 'successful-ok',
                             'Successful': True}
        assert response == expected_response, response

    @tornado.testing.gen_test
    def test_async_timeout_call(self):
        from pyipptool.core import AsyncIPPToolWrapper, TimeoutError
        from pyipptool.forms import get_subscriptions_form

        class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
            """
            HTTP Handler that will make ipptool waiting
            """
            protocol_version = 'HTTP/1.1'

            def do_POST(self):
                time.sleep(0.2)
                assassin = threading.Thread(target=self.server.shutdown)
                assassin.daemon = True
                assassin.start()

        PORT = 6789
        while True:
            try:
                httpd = SocketServer.TCPServer(("", PORT), Handler)
            except socket.error as exe:
                if exe.errno in (48, 98):
                    PORT += 1
                else:
                    raise
            else:
                break
        httpd.allow_reuse_address = True

        thread = threading.Thread(target=httpd.serve_forever)
        thread.daemon = True
        thread.start()

        wrapper = AsyncIPPToolWrapper(self.config, self.io_loop)
        wrapper.config['cups_uri'] = 'http://localhost:%s/' % PORT
        request = get_subscriptions_form.render(
            {'header':
             {'operation_attributes':
              {'printer_uri': 'http://localhost:%s/printers/fake' % PORT}}}
        )

        try:
            old_timeout = wrapper.config['timeout']
            wrapper.config['timeout'] = .1
            with pytest.raises(TimeoutError):
                yield wrapper._call_ipptool(request)
        finally:
            wrapper.config['timeout'] = old_timeout
