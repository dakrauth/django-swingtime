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


Running the Tests
=================

.. note::

    From the ``django-swingtime`` root directory

::

    $ cd tests
    $ python manage.py test swingtime
    $ ./cover # <-- run `coverage`
    $ cd ../
    $ tox


