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

Setup a virtual environment::

    $ mkvirtualenv swingtime
    $ pip install invoke

Get the code:

* ``git``::

    $ git clone https://github.com/dakrauth/django-swingtime.git django-swingtime
    $ cd django-swingtime

* Download::

    $ curl -o swingtime.zip -L https://github.com/dakrauth/django-swingtime/archive/master.zip
    $ unzip swingtime.zip
    $ cd django-swingtime-master

``Invoke`` is used to automate many tasks. See ``inv -l`` for all options.::

    $ inv dev


Documentation
=============

.. note::

    Building the documentation requires `Sphinx <http://www.sphinx-doc.org/>`_ to be installed.

First, install the ``swingtime`` project as shown in :ref:`development`.::

    $ inv docs

Browse the file ``docs/index.html``.


Running the Tests
=================

First, install the ``swingtime`` project as shown in :ref:`development`.::

    $ inv test

