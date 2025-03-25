============
Installation
============

Get ``Swingtime``
=================

Basic Installation
------------------

Install into the current environment::

    $ pip install django-swingtime

.. _development:

Development
===========

* Get the code::

    $ git clone https://github.com/dakrauth/django-swingtime.git django-swingtime
    $ cd django-swingtime

* Or, download::

    $ curl -o swingtime.zip -L https://github.com/dakrauth/django-swingtime/archive/main.zip
    $ unzip swingtime.zip
    $ cd django-swingtime-main

* Environment::

    $ python -m venv venv
    $ . venv/bin/activate
    $ ./run init

* Test

    Assuming you have `pyenv <https://github.com/pyenv/pyenv>`_ installed and the
    following versions installed (``x`` would be your installed patch version)::

        $ pyenv local 3.10.x 3.11.x 3.12.x 3.13.x
        $ ./run test

    Or, to directly interface with tox::

        $ tox  # or...
        $ tox -e py313-django5.2  # build and test only Python 3.13 and Django 5.2
    

* Documentation

    ::

        $ ./run docs

    Browse the file ``docs/index.html``.
