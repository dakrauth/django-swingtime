Demo
====

Swingtime comes with its own demo project and application. The demo is themed as
a Karate studio's website and allows you see and interact with the Swingtime
application.

Within the Swingtime demo is an app named ``karate``, which defines the custom
management command ``loaddemo``. This command will pre-populate your
initial database with some events and occurrences based upon the current date and
time.

Currently, Swingtime does not include any templates of its own. The demo project
provides some sample templates to use as a guide or starting point.

The easiest way to run the demo is to use Docker::

.. code:: bash

    $ docker build -t swingtime .
    $ docker run -p 8000:80 -d swingtime:latest

And browse to `localhost:8000 <http://localhost:8000>`_.
