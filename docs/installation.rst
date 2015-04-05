Installation
============

Get ``Swingtime``
-----------------

Options:

* Source: https://github.com/dakrauth/django-swingtime
* ``pip install django-swingtime``
* ``curl -o swingtime.zip -L https://github.com/dakrauth/django-swingtime/archive/master.zip``


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

Get the code::

    $ git clone https://github.com/dakrauth/django-swingtime.git django-swingtime-master


*-- or --*

::

    $ curl -o swingtime.zip -L https://github.com/dakrauth/django-swingtime/archive/master.zip
    $ unzip swingtime.zip
    $ cd 


And::

    $ cd django-swingtime-master


You can set up your environment to run the demo in a ``virtualenv`` by doing the
following (please note that for the following commands you have already installed
``virtualenv`` and ``virtualenvwrapper``)::

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

*From the* ``django-swingtime-master`` *directory*

* Build the documentation files as HTML::

    $ cd docs && make html

* Run development server to check for deprecation warning::

    $ python -Wd manage.py runserver

* Run the tests::

    $ cd tests
    $ python manage.py test swingtime
    $ ./cover # <-- run `coverage`
    $ cd ../
    $ tox


