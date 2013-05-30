# Installation

- [Debian](#ubuntudebian)
- [Ubuntu](#ubuntudebian)
- [Archlinux](#archlinux)
- [Heroku](#heroku)
- [Others](#others)

Leselys use [Supervisor](http://supervisord.org/) in order to manage these processes.
Step will be explain for your system.

## Ubuntu/Debian

You just need ``root`` or ``sudo`` access.
All of dependencies are available with ``apt-get`` and Python dependencies will be installed with ``pip``.

For Ubuntu, these guide consider you do ``sudo`` or you have done ``sudo su -`` at the beginning.

```
$ apt-get install build-essential python-dev python-setuptools
$ apt-get install libxslt1-dev libxml2-dev
$ apt-get install supervisor
$ easy_install pip
$ pip virtualenv
```

Install Mongodb for [Ubuntu](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/) and for [Debian](http://docs.mongodb.org/manual/tutorial/install-mongodb-on-debian/).

```
$ adduser --system --home /var/www/leselys --disabled-password leselys
```

And now Leselys (as ``leselys`` user):

```
$ su - leselys
virtualenv .
source bin/activate
pip install leselys
leselys init leselys.ini
```

As ``root``:

```
$ wget https://raw.github.com/socketubs/leselys/master/supervisor.conf --output-file /etc/supervisor/conf.d/leselys.conf
$ service supervisor restart
```

## Archlinux

Siosm have made an Archlinux package on ``aur`` which you can install like that:

```
yaourt -S leselys-git
```

## Heroku

This installation use ``git`` version of Leselys. Try to update your installation just when I a release or be sure of what you do.

Heroku installation require Redis for session, cause process hibernate will break all session if we use memory.
You will also need the Heroku Scheduler add-on to refresh your feeds.

All Heroku dependencies like ``Pymongo``, ``gunicorn`` and ``redis`` are in ``requirements.txt`` file, so everything will be installed automagically.

```
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
```

## Others

You need to have the following things installed and ready to use:

- Python2.6 (*not verified*) at least
- Python headers (for compiling)
- [supervisor](http://supervisord.org/) via package manager or ``pip``
- ``easy_install`` or ``pip``
- [MongoDB](http://docs.mongodb.org/manual/installation/)

And you just have to run:

```
pip install virtualenv
# or easy_install virtualenv
cd /var/www
virtualenv leselys
source leselys/bin/activate
pip install leselys
```
