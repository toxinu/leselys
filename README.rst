Leselys
=======

I'm Leselys, your very elegant RSS reader. No bullshit Android, iPhone apps, just a responsive design for every device.

Leselys is Heroku ready and easy to install. It can be used with your very own storage backend. Take a look at the `MongoDB`_ example.

There is a `demo here`_ (demo/demo).

Leselys is in heavy development right now, and feedback is welcome.

Installation
------------

Quick local setup (with sofart backend):

Ubuntu
~~~~~~

::

	apt-get install build-essential python-dev python-pip
	apt-get install libxslt1-dev libxml2-dev python-libxml2 python-libxslt1

And finally: ::

	pip install leselys
	pip install sofart
	leselys init --config leselys.ini
	leselys adduser --config leselys.ini
	leselys serve --config leselys.ini

Open your browser at ``http://localhost:5000``.

Import your Google Reader OPML file right now!

Heroku
~~~~~~

Advanced setup with MongoDB for storage and Redis for session on Heroku.
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

License
-------

License is `AGPL3`_. See `LICENSE`_.

.. _demo here: https://leselys.herokuapp.com
.. _MongoDB: https://github.com/socketubs/leselys/blob/master/leselys/backends/_mongodb.py
.. _AGPL3: http://www.gnu.org/licenses/agpl.html
.. _LICENSE: https://raw.github.com/socketubs/leselys/master/LICENSE
