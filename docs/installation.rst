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

.. _full-project-source-install:

Full project source code
------------------------

* ``git``::

    $ git clone https://github.com/dakrauth/django-swingtime.git django-swingtime
    $ cd django-swingtime

* Download::

    $ curl -o swingtime.zip -L https://github.com/dakrauth/django-swingtime/archive/master.zip
    $ unzip swingtime.zip
    $ cd django-swingtime-master


Documentation
=============

.. note::

    Building the documentation requires `Sphinx <http://www.sphinx-doc.org/>`_ to be installed.

Install the ``swingtime`` project as shown in :ref:`full-project-source-install`
and build the docs as follows::

    $ cd docs
    $ make html

Browse the file ``build/html/index.html``.


Demo
====

Intro
-----

Swingtime comes with its own demo project and application. The demo is themed as 
a Karate studio's website and allows you see and interact with the Swingtime
application.

Within the Swingtime demo is an app named ``karate``, which defines the custom
management command ``loaddemo``. This command will pre-populate your 
initial database with some events and occurrences based upon the current date and
time.

Currently, Swingtime does not include any templates of its own. The demo project
provides some sample templates to use as a guide or starting point.

Running the demo
----------------

Install the ``swingtime`` project as shown in :ref:`full-project-source-install`.
You can set up your environment to run the demo in a ``virtualenv`` by doing the
following from the root ``swingtime`` project directory::

    $ mkvirtualenv swingtime_demo
    $ pip install -r requirements.txt
    $ cd demo
    $ python manage.py loaddemo
    $ python manage.py runserver


``loaddemo`` is just a simple wrapper around ``syncdb`` and a short script to load
some data into your new database (by default, a sqlite3 database named ``karate.db``)
in the root directory of the demo.

Now, you are ready to browse to http://127.0.0.1:8000/

Optional
--------

.. note::

    From the ``django-swingtime`` root directory

* Run development server to check for deprecation warning::

    $ python -Wd manage.py runserver

* Run the tests::

    $ cd tests
    $ python manage.py test swingtime
    $ ./cover # <-- run `coverage`
    $ cd ../
    $ tox


