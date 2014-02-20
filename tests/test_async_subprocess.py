import BaseHTTPServer
import os
import SocketServer
import socket
import threading
import time

from pkipplib import pkipplib
import pytest
import tornado.testing


NO_TORNADO = os.getenv('NO_TORNADO', '').lower() in ('1', 'yes', 'true', 't')


@pytest.mark.skipif(NO_TORNADO, reason='requires tornado')
class AsyncSubprocessTestCase(tornado.testing.AsyncTestCase):

    @tornado.testing.gen_test
    def test_async_call(self):
        from pyipptool import wrapper
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

        request = get_subscriptions_form.render(
            {'header':
             {'operation_attributes':
              {'printer_uri': 'http://localhost:%s/printers/fake' % PORT}}}
        )

        try:
            wrapper.io_loop = self.io_loop
            response = yield wrapper._call_ipptool(
                'http://localhost:%s/' % PORT, request)
        finally:
            wrapper.io_loop = None
            try:
                del response['Tests'][0]['RequestId']
            except KeyError:
                self.fail(response)
            assert response == {'Successful': True,
                                'Tests':
                                [{'Name': 'Get Subscriptions',
                                  'Operation': 'Get-Subscriptions',
                                  'Version': '1.1',
                                  'RequestAttributes':
                                  [{'attributes-charset': 'utf-8',
                                    'attributes-natural-language': 'en',
                                    'printer-uri':
                                    'http://localhost:%s/printers/fake' % PORT}
                                   ],
                                  'ResponseAttributes':
                                  [{'attributes-charset': 'utf-8',
                                    'attributes-natural-language': 'en-us'}
                                   ],
                                    'StatusCode': 'successful-ok',
                                    'Successful': True}],
                                'Transfer': 'auto',
                                'ipptoolVersion': 'CUPS v1.7.0'}, response

    @tornado.testing.gen_test
    def test_async_timeout_call(self):
        from pyipptool import wrapper
        from pyipptool.core import TimeoutError
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

        request = get_subscriptions_form.render(
            {'header':
             {'operation_attributes':
              {'printer_uri': 'http://localhost:%s/printers/fake' % PORT}}}
        )

        try:
            old_timeout = wrapper.config['timeout']
            wrapper.config['timeout'] = .1
            wrapper.io_loop = self.io_loop
            with pytest.raises(TimeoutError):
                yield wrapper._call_ipptool('http://localhost:%s/' % PORT,
                                            request)
        finally:
            wrapper.io_loop = None
            wrapper.config['timeout'] = old_timeout
