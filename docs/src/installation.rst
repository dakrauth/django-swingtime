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
    $ pip install tox
    $ tox -e dev

* Test

    Assuming you have `pyenv <https://github.com/pyenv/pyenv>`_ installed and the
    following versions installed (``x`` would be your installed patch version)::

        $ pyenv local 3.8.x 3.9.x 3.10.x 3.11.x 3.12.x
        $ tox  # or...
        $ tox -e py38-django3.2  # build and test only Python 3.8 and Django 3.2

* Documentation

    ::

        $ tox -e docs

    Browse the file ``docs/index.html``.
