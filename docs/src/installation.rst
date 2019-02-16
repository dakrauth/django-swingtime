============
Installation
============

.. note::

    The ``swingtime`` documentation assumes familiarity with and installation of
    Python deployment tools `pip <https://pip.pypa.io>`_,
    `virtualenv <https://virtualenv.pypa.io/>`_, and
    `virtualenvwrapper <https://bitbucket.org/dhellmann/virtualenvwrapper>`_.


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

    $ curl -o swingtime.zip -L https://github.com/dakrauth/django-swingtime/archive/master.zip
    $ unzip swingtime.zip
    $ cd django-swingtime-master

* Environment::

    $ python -m venv venv
    $ . venv/bin/activate
    $ pip install tox
    $ tox -e dev

* Test

    Assuming you have `pyenv <https://github.com/pyenv/pyenv>`_ installed and the
    following versions installed::

        $ pyenv local 3.7.2 3.4.9 3.5.6 3.6.8
        $ tox  # or...
        $ tox -e py37-django2.1  # build and test only Python 3.7 and Django 2.1

* Documentation

    ::

        $ tox -e docs

    Browse the file ``docs/index.html``.
