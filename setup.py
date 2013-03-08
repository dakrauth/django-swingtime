#!/usr/bin/env python
from distutils.core import setup

VERSION = '0.2.1' 

setup(
    name='django-swingtime',
    version=VERSION,
    url='https://github.com/dakrauth/django-swingtime',
    author_email='dakrauth@gmail.com',
    description='A Django calendaring application.',
    long_description='Swingtime is a Django application similar to a stripped down version of iCal for Mac OS X or Google Calendar',
    author='David A Krauth',
    platforms=['any'],
    packages=[
        'swingtime',
        'swingtime.conf'
    ],
)
