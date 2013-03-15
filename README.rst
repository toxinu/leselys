Leselys
=======

I'm Leselys, your very elegant RSS reader.

Leselys can be used with your very own backend, take a look at `Mongodb`_ example.

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

Open your brower at ``http://localhost:5000``.

License
-------

License is `AGPL3`_. See `LICENSE`_.

.. _Mongodb: https://github.com/socketubs/leselys/blob/master/leselys/backends/_mongodb.py
.. _AGPL3: http://www.gnu.org/licenses/agpl.html
.. _LICENSE: https://raw.github.com/socketubs/leselys/master/LICENSE
