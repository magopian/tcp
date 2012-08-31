proj = tcp
settings = --settings=$(proj).settings
test_settings = --settings=$(proj).test_settings


test:
	django-admin.py test core $(test_settings) --failfast --noinput

run:
	foreman start

db:
	django-admin.py syncdb $(settings)

migrate:
	django-admin.py migrate $(settings)

user:
	django-admin.py createsuperuser $(settings)

shell:
	django-admin.py shell $(settings)

dbshell:
	django-admin.py dbshell $(settings) 

makemessages:
	cd $(proj) && django-admin.py makemessages -a $(settings)

compilemessages:
	cd $(proj) && django-admin.py compilemessages $(settings)

sdist:
	python setup.py sdist
