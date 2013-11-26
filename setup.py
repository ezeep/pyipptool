import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


version = '0.1.dev'

setup(
    name='pyipptool',
    version=version,
    author='Nicolas Delaby',
    author_email='nicolas.delaby@ezeep.com',
    packages=('pyipptool',),
    install_requires=('deform',),
    tests_require=('mock', 'pytest'),
    include_package_data=True,
    test_suite='tests',
    cmdclass = {'test': PyTest},
)
