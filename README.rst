TopCodingParty
==============

.. image:: https://secure.travis-ci.org/magopian/tcp.png
   :alt: Build Status
   :target: https://secure.travis-ci.org/magopian/tcp

TCP is the accronym of TopCodingParty, http://topcodingparty.net.

The project stack is:

* backend: `Django`_, a `Python`_ based web development framework for
  perfectionists with deadlines

* frontend: `HTML5 Boilerplate`_ for the containing templates, `Twitter
  Bootstrap`_ for the layout and styling, `SASS`_ compiled CSS

.. _Django: http://djangoproject.com
.. _Python: http://python.org
.. _`HTML5 Boilerplate`: http://html5boilerplate.com/
.. _`Twitter Bootstrap`: http://twitter.github.com/bootstrap/
.. _SASS: http://sass-lang.com/


Some of its features:

* Rate limited login

* Error logging using `Sentry`_

* Makes use of HTML5, CSS3

* Easy two-step registration

.. _Sentry: http://getsentry.com

Installation
------------

Getting the code::

    git clone git@github.com:magopian/tcp.git
    cd tcp
    virtualenv -p python2 env
    source env/bin/activate
    add2virtualenv .
    pip install -r requirements.txt

Configuration
-------------

Create ``tcp/settings.py`` and put the minimal stuff in it::

    from default_settings import *

    ADMINS = (
        ('Your name', 'email@example.com'),
    )
    MANAGERS = ADMINS

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'tcp',
            'USER': 'postgres',
        },
    }

    SECRET_KEY = 'something secret'

    TIME_ZONE = 'Europe/Paris'

    EMAIL_HOST = 'mail.your_domain.com'
    EMAIL_SUBJECT_PREFIX = '[TCP] '

For Readability, Instapaper and Pocket support, you'll need a couple of
additional settings::

    API_KEYS = {
        'readitlater': 'your readitlater (pocket) key',
    }

    INSTAPAPER = {
        'CONSUMER_KEY': 'yay isntappaper',
        'CONSUMER_SECRET': 'secret',
    }

    READABILITY = {
        'CONSUMER_KEY': 'yay readability',
        'CONSUMER_SECRET': 'othersecret',
    }

Then deploy the Django app using the recipe that fits your installation (with
mod_wsgi or mod_fcgi). More documentation on the `Django deployment guide`_.

.. _Django deployment guide: http://docs.djangoproject.com/en/dev/howto/deployment/

Once your application is deployed (you've run
``django-admin.py syncdb --settings=feedhq.settings`` to create the database
tables), you can add users to the application. On the admin interface, add as
many users as you want. When you've added some categories and feeds to your
account, you can crawl for updates::

    django-admin.py updatefeeds --settings=feedhq.settings

Set up a cron job to update your feeds on a regular basis. This puts the
last-updated feeds in the update queue::

    */5 * * * * /path/to/env/django-admin.py updatefeeds --settings=feedhq.settings

A cron job should also be set up for picking and updating favicons (the
``--all`` switch processes existing favicons in case they have changed)::

    @daily /path/to/env/bin/django-admin.py favicons --settings=feedhq.settings
    @monthly /path/to/env/bin/django-admin.py favicons --all --settings=feedhq.settings

And another job for checking feeds that have been muted because they were
failing too much::

    @daily /path/to/env/bin/django-admin.py check_defunct --settings=feedhq.settings

And a final one to purge expired sessions from the DB::

    @daily /path/to/env/bin/django-admin.py cleanup --settings=feedhq.settings

Development
-----------

Install the development requirements::

    pip install -r requirements-dev.txt

Run the tests::

    make test

Or if you want to run the tests with ``django-admin.py`` directly, make sure
you use ``feedhq.test_settings`` to avoid making network calls while running
the tests.

If you want to contribute and need an environment more suited for development,
you can use the ``settings.py`` file to alter default settings. For example,
to enable the `django-debug-toolbar`_::

    MIDDLEWARE_CLASSES += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INTERNAL_IPS = ('127.0.0.1',)

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'HIDE_DJANGO_SQL': False,
    }

.. _django-debug-toolbar: https://github.com/robhudson/django-debug-toolbar

When running ``django-admin.py updatefeeds`` on your development machine,
make sure you have ``DEBUG = True`` in your settings to avoid making
PubSubHubbub subscription requests without any valid callback URL.
