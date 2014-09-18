#!/usr/bin/env python
import os, sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit(0)

with open('README.rst', 'r') as f:
    long_description = f.read()

# Dynamically calculate the version based on swingtime.VERSION.
VERSION = __import__('swingtime').get_version()

setup(
    name='django-swingtime',
    version=VERSION,
    url='https://github.com/dakrauth/django-swingtime',
    author_email='dakrauth@gmail.com',
    description='A Django calendaring application.',
    long_description=long_description,
    author='David A Krauth',
    platforms=['any'],
    license='MIT License',
    classifiers=(
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ),
    packages=['swingtime', 'swingtime.conf'],
    install_requires=['python-dateutil', 'django>=1.5']
)
