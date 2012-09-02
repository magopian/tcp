TopCodingParty
==============

Find the documentation at http://top-coding-party.readthedocs.org/en/latest/.

.. image:: https://secure.travis-ci.org/magopian/tcp.png
   :alt: Build Status
   :target: https://secure.travis-ci.org/magopian/tcp

TCP is the accronym of TopCodingParty, http://topcodingparty.net.

The project stack is based on

* backend: Django_, a Python_ based web development framework for
  perfectionists with deadlines

* frontend: `HTML5 Boilerplate`_ for the containing templates, `Twitter
  Bootstrap`_ for the layout and styling, SASS_ compiled CSS

.. _Django: http://djangoproject.com
.. _Python: http://python.org
.. _`HTML5 Boilerplate`: http://html5boilerplate.com/
.. _`Twitter Bootstrap`: http://twitter.github.com/bootstrap/
.. _SASS: http://sass-lang.com/


Some of its features:

* Rate limited login

* Error logging using Sentry_

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

    ADMINS = ( ('Your name', 'email@example.com'),
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


Then deploy your application and run
``django-admin.py syncdb --settings=tcp.settings`` to create the database
tables, then ``django-admin.py migrate --settings=tcp.settings`` to run all
South_ migrations.

.. _South: http://south.readthedocs.org/en/latest/

The very first time you launch the application, once the database is set up,
you may want to load some example providers and matches. To do that, use the
following command::

    django-admin.py loaddata providers_matches.json --settings=tcp.settings

Be aware that if you do that again later, it will simply overwrite the entries,
loosing your modifications to those entries, if any.


Development
-----------

Install the development requirements::

    pip install -r requirements-dev.txt

Run the tests::

    make test

Or if you want to run the tests with ``django-admin.py`` directly, make sure
you use ``tcp.test_settings``.

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


Development goodies
-------------------

There's an improved flow all set up just for ease of development, with Foreman_
and Gorun_. This flow has been inspired by `Bruno Renié`_:

* make gems play nice with virtualenv. Add this to your venv/bin/postactivate
  script::

    export GEM_HOME="$VIRTUAL_ENV/gems"
    export GEM_PATH=""
    export PATH=$PATH:$GEM_HOME/bin

* install the gems::

    gem install bundler
    bundle install

* start Foreman (which will start the development server, compile SASS files
  each time they're modified, run the tests on each code change)::

    foreman start

.. _Foreman: https://github.com/ddollar/foreman#readme
.. _Gorun: https://github.com/peterbe/python-gorun#readme
.. _`Bruno Renié`: http://bruno.im/2011/sep/29/streamline-your-django-workflow/


Wishlist / ToDo
---------------

* make the validation optional (validation is costly), or even in another
  endpoint
* put together a compatibility matrix for the following platforms:
    - Internet explorer 6
    - Firefox 3
    - Chrome
    - Safari
    - Opera
    - iOS
    - Android
* improve the validation "algorithm" to take corner cases into account
