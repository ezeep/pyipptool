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


version = '0.3'


def read_that_file(path):
    with open(path) as open_file:
        return open_file.read()


description = '\n'.join((read_that_file('README.rst'),
                         read_that_file('LICENSE.txt')))

setup(
    name='pyipptool',
    version=version,
    author='Nicolas Delaby',
    author_email='nicolas.delaby@ezeep.com',
    description='ipptool python wrapper',
    url='https://github.com/ezeep/pyipptool',
    long_description=description,
    license=' Apache Software License',
    packages=('pyipptool',),
    install_requires=('deform',),
    tests_require=('mock', 'pytest', 'coverage',
                   'pytest-cov', 'coveralls'),
    include_package_data=True,
    test_suite='tests',
    cmdclass = {'test': PyTest},
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Printing',
    ]
)
