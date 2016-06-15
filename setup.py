#!/usr/bin/env python
# encoding:utf-8
import os
import re

from setuptools import setup
from setuptools import find_packages

PROJECT_NAME = 'a2billing_spyne'

v = open(os.path.join(os.path.dirname(__file__), PROJECT_NAME, '__init__.py'), 'r')
VERSION = re.match(r".*__version__ = '(.*?)'", v.read(), re.S).group(1)

LONG_DESC = ""
try:
    os.stat('CHANGELOG.rst')
    LONG_DESC = open('CHANGELOG.rst', 'r').read()
except OSError:
    pass


setup(
    name=PROJECT_NAME,
    packages=find_packages(),
    version=VERSION,
    description="This is a caching PyPI implementation that uses Spyne",
    long_description=LONG_DESC,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Intended Audience :: Developers',
    ],
    keywords=('spyne', 'asterisk'),
    author=u'Cemrecan Ünal',
    author_email='unalcmre@gmail.com',
    url='http://github.com/cemrecan/a2billing-spyne',
    license='GPL',

    install_requires=['spyne', 'sqlalchemy', 'neurons'],

    include_package_data=True,
    package_data={
        "a2billing_spyne.const": [
            "index.html",
        ],
    },

    entry_points = {
        'console_scripts': [
            'a2bs_daemon=%(p)s.main:main' % {'p': PROJECT_NAME},
        ]
    },
)
