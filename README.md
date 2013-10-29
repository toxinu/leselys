## Installation

	virtualenv virtenv
	source virtenv/bin/activate
	pip install -r requirements.txt
	python manage.py syncdb
	python manage.py migrate
	python manage.py loaddata initial
