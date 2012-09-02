TopCodingParty
==============

TCP is a web REST service, that you can use to update and validate video embed
codes from video providers (think Youtube, Dailymotion, Vimeo...).

The source code is hosted on `github`_.

.. _github: https://github.com/magopian/tcp

Installation
------------

Getting the code::

    git clone git@github.com:magopian/tcp.git
    cd tcp
    virtualenv -p python2 env
    source env/bin/activate
    add2virtualenv .
    pip install -r requirements.txt

Deployment
----------

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


.. toctree::
   :maxdepth: 2

   manual_usage
   api_usage
   administration
