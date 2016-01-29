#!/usr/bin/env python
import os, sys
from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit(0)

with open('README.rst', 'r') as f:
    long_description = f.read()

# Dynamically calculate the version based on swingtime.VERSION.
version=__import__('swingtime').get_version()

setup(
    name='django-swingtime',
    url='https://github.com/dakrauth/django-swingtime',
    author='David A Krauth',
    author_email='dakrauth@gmail.com',
    description='A Django calendaring application.',
    version=version,
    long_description=long_description,
    platforms=['any'],
    license='MIT License',
    classifiers=(
        'Environment :: Web Environment',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ),
    packages=find_packages(),
    package_data={'swingtime': ['locale/*/*/*.*', 'fixtures/swingtime_test.json']},
    requires=['dateutil', 'django']
)
