Leselys
=======

I'm Leselys, your very elegant RSS reader.

No `bullshit apps`_ for Android, iPhone, etc. Just a responsive design and for every device.

Tere is a `demo here`_ (demo/demo).

Installation
------------

Two requirements: __Mongodb__ and __Python__.

::

	pip install leselys
	leselys init leselys.ini
	leselys adduser leselys.ini
	leselys serve leselys.ini

	leselys worker leselys.ini

Open your browser at ``http://localhost:5000``.

Import your Google Reader OPML file right now!

Help
~~~~

* `Ubuntu`_
* `Heroku`_


Misc
----

Storage and session backends are Python modules, you can easily write your own. Take a look at the `MongoDB`_ storage backend.

License
-------

License is `AGPL3`_. See `LICENSE`_.

.. _bullshit apps: http://tommorris.org/posts/8070
.. _demo here: https://leselys.herokuapp.com
.. _MongoDB: https://github.com/socketubs/leselys/blob/master/leselys/backends/_mongodb.py
.. _Ubuntu: https://github.com/socketubs/leselys/tree/master/docs/ubuntu.rst 
.. _Heroku: https://github.com/socketubs/leselys/tree/master/docs/heroku.rst
.. _AGPL3: http://www.gnu.org/licenses/agpl.html
.. _LICENSE: https://raw.github.com/socketubs/leselys/master/LICENSE
