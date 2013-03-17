Leselys
=======

I'm Leselys, your very elegant RSS reader. No bullshit Android, iPhone apps, just a responsive design for every device.

Leselys can be used with your very own backend. Take a look at the `MongoDB`_ example.

There is a `demo here`_ (demo/demo).

Leselys is in heavy development right now, and feedback is welcome.

Installation
------------

::

	pip install leselys

Usage
-----

::

  echo_leselys_conf > leselys.ini
  leselys adduser --config leselys.ini
  leselys serve --config leselys.ini

Open your browser at ``http://localhost:5000``.

Import your Google Reader OPML file right now!

Heroku
~~~~~~

::

	heroku create
	heroku addons:add mongohq:sandbox
	git push heroku master

Don't forget to create a Leselys account with ``heroku run "bash heroku.sh && leselys adduser --config heroku.ini"``.

License
-------

License is `AGPL3`_. See `LICENSE`_.

.. _demo here: https://leselys.herokuapp.com
.. _MongoDB: https://github.com/socketubs/leselys/blob/master/leselys/backends/_mongodb.py
.. _AGPL3: http://www.gnu.org/licenses/agpl.html
.. _LICENSE: https://raw.github.com/socketubs/leselys/master/LICENSE
