Leselys
=======

I'm Leselys, your very elegant RSS reader.

No `bullshit apps`_ for Android, iPhone, etc. Just a responsive design and for every device.

Leselys is Heroku ready. There is a `demo here`_ (demo/demo).

Installation
------------

Ubuntu
~~~~~~

Two requirements: **Mongodb** and **Python**.

In order to install leselys you'll need some dependencies: ::

  apt-get install build-essential python-dev python-pip
  apt-get install libxslt1-dev libxml2-dev python-libxml2 python-libxslt1

And install your `MongoDB`_.


::

  pip install leselys
  leselys init leselys.ini
  leselys adduser leselys.ini
  leselys serve leselys.ini
  # In another terminal
  leselys worker leselys.ini

Open your browser at ``http://localhost:5000``.


Heroku
~~~~~~

Advanced setup with MongoDB for storage and Redis for session on Heroku.
You will also need the Heroku Scheduler add-on to refresh your feeds.

All Heroku dependencies like ``Pymongo``, ``gunicorn`` and ``redis`` are in ``requirements-heroku.txt`` file.

::

  git clone git@github.com:socketubs/leselys.git
  cd leselys
  heroku create
  heroku addons:add mongohq:sandbox
  heroku addons:add redistogo:nano
  heroku addons:add scheduler:standard
  heroku addons:open scheduler
  # Add "sh heroku.sh && leselys refresh heroku.ini" job every 10 minutes
  # And "sh heroku.sh && leselys retention heroku.ini" job every day
  git push heroku master

Don't forget to create a Leselys account with ``heroku run "bash heroku.sh && leselys adduser heroku.ini"``.

Import your Google Reader OPML file right now!

Misc
----

Storage and session backends are Python modules, you can easily write your own. Take a look at the `MongoDB storage backend`_.
