#!/usr/bin/env python
import os, sys
from setuptools import setup, find_packages


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
    python_requires='>=3.10, <4',
    install_requires=['Django>=4.2,<5.2', 'python-dateutil>=2.8.2'],
    extras_require={
        'test': ['tox', 'coverage', 'pytest-django', 'pytest', 'pytest-cov', 'flake8'],
        'docs': ["sphinx", "sphinx-rtd-theme"]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Framework :: Django :: 5.1',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Office/Business :: Scheduling',
    ],
    packages=find_packages(),
    package_data={'swingtime': ['locale/*/*/*.*',]},
    zip_safe=False,
)
