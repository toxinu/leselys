Heroku [WIP]
~~~~~~~~~~~~

Advanced setup with MongoDB for storage and Redis for session on Heroku.
You will also need a second Dyno in order to have your refresher.

All Heroku dependencies like ``Pymongo``, ``gunicorn`` and ``redis`` are in ``requirements-heroku.txt`` file.

::

	git clone git@github.com:socketubs/leselys.git
	cd leselys
	cp requirements-heroku.txt requirements.txt
	heroku create
	heroku addons:add mongohq:sandbox
	heroku addons:add redistogo:nano
	git push heroku master

Don't forget to create a Leselys account with ``heroku run "bash heroku.sh && leselys adduser --config heroku.ini"``.