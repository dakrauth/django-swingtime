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
    long_description_content_type='text/x-rst',
    platforms=['any'],
    license='MIT License',
    python_requires='>=3.6, <4',
    install_requires=['Django>=2.2,<4.0', 'python-dateutil==2.8.0'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Framework :: Django :: 3.2',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Office/Business :: Scheduling',
    ],
    packages=find_packages(),
    package_data={'swingtime': ['locale/*/*/*.*',]},
    zip_safe=False,
)
