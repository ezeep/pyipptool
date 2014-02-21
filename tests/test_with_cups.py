import os

import pytest

TRAVIS = os.getenv('TRAVIS')
TRAVIS_USER = os.getenv('USER')
TRAVIS_BUILD_DIR = os.getenv('TRAVIS_BUILD_DIR')


@pytest.mark.skipif(TRAVIS != 'true', reason='requires travis')
class TestWithCups(object):

    ipptool_path = '%s/ipptool-20130731/ipptool' % TRAVIS_BUILD_DIR
    config = {'ipptool_path': ipptool_path,
              'login': TRAVIS_USER,
              'password': 'travis',
              'graceful_shutdown_time': 2,
              'timeout': 5}

    def test_cups_get_printers(self):
        import pyipptool
        ipptool = pyipptool.core.IPPToolWrapper(self.config)
        response = ipptool.cups_get_printers('http://localhost:631/')
        assert response['Name'] == 'CUPS Get Printers'
        assert response['Operation'] == 'CUPS-Get-Printers'
        assert response['RequestAttributes'] == [{
            'attributes-charset': 'utf-8',
            'attributes-natural-language': 'en'}]
        assert len(response['ResponseAttributes']) == 2
        assert response['ResponseAttributes'][1]['printer-name'] == 'PDF'
        assert response['StatusCode'] == 'successful-ok'
        assert response['Successful']

    def test_cups_get_ppds(self):
        import pyipptool
        ipptool = pyipptool.core.IPPToolWrapper(self.config)
        response = ipptool.cups_get_ppds('http://localhost:631/',
                                         ppd_make_and_model='generic pdf')
        assert response['Name'] == 'CUPS Get PPDs'
        assert response['Operation'] == 'CUPS-Get-PPDs'
        assert response['RequestAttributes'] == [{
            'attributes-charset': 'utf-8',
            'attributes-natural-language': 'en',
            'ppd-make-and-model': 'generic pdf'}]
        assert len(response['ResponseAttributes']) == 2
        assert 'ppd-make-and-model' in response['ResponseAttributes'][1]
        ppd = response['ResponseAttributes'][1]
        assert ppd['ppd-make-and-model'] == 'Generic PDF Printer'
        assert response['StatusCode'] == 'successful-ok'
