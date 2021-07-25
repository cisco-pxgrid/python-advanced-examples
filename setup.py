#
# Copyright (c) 2021 Cisco and/or its affiliates
#
import os
import sys
import versioneer
from setuptools import setup


#
# hack to provent incorrect shebang substitution
#
import re
from distutils.command import build_scripts
build_scripts.first_line_re = re.compile(b'^should not match$')


__author__ = "Einar Nilsen-Nygaard"
__author_email__ = "einarnn@cisco.com"
__copyright__ = "Copyright (c) 2021 Cisco and/or its affiliates."
__license__ = "Apache 2.0"


if (sys.version_info.major == 2) or (sys.version_info.major == 3 and sys.version_info.minor < 8):
    print ("Sorry, Python < 3.8 is not supported")
    exit()


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='pxgrid_util',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description=('A utility library and example scripts for Cisco pxGrid 2.0'),
    long_description='A utility library and example scripts for Cisco pxGrid 2.0',
    packages = ['pxgrid_util'],
    scripts=[
        'bin/anc-policy',
        'bin/matrix-query-all',
        'bin/profiles-query-all',
        'bin/px-subscribe',
        'bin/session-query-all',
        'bin/session-query-by-ip',
        'bin/sgacls-query-all',
        'bin/sgts-query-all',
        'bin/sxp-query-bindings',
        'bin/system-query-all',
        'bin/user-groups-query',
    ],
    author=__author__,
    author_email=__author_email__,
    license=__license__ + "; " + __copyright__,
    url='https://github.com/cisco-pxgrid/python-advanced-examples',
    download_url='https://github.com/cisco-pxgrid/python-advanced-examples',
    install_requires=[
        'websockets>=9.1',
    ],
    include_package_data=True,
    platforms=["Posix; OS X; Windows"],
    keywords=['ISE', 'pxGrid'],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
