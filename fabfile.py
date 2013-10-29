import os
import sys
from fabric.api import task
from fabric.api import local


def check_virtualenv():
    if not os.path.exists('virtenv'):
        print(' !! I need a virtualenv (virtenv). Run "fab init_virtualenv".')
        sys.exit(1)


@task
def update_requirements(env="dev"):
    check_virtualenv()
    local('virtenv/bin/pip install -r requirements/%s.txt' % env)


@task
def runserver(env="dev", ip='127.0.0.1', port=8000, workers=2):
    check_virtualenv()
    if env == 'prod':
        virtualenv('gunicorn leselys.wsgi:application --workers=%s -b %s:%s' % (workers, ip, port))
    else:
        local('virtenv/bin/python manage.py runserver %s:%s --settings=leselys.settings_%s' % (ip, port, env))


@task
def runcelery():
    check_virtualenv()
    local('virtenv/bin/python manage.py celeryd -B --settings=leselys.settings_dev')


@task
def syncdb(env="dev"):
    check_virtualenv()
    local("virtenv/bin/python manage.py syncdb --settings='leselys.settings_%s'" % env)
    local("virtenv/bin/python manage.py migrate --settings='leselys.settings_%s'" % env)


@task
def collectstatic(env="dev"):
    check_virtualenv()
    if env == "prod":
        local('heroku run python manage.py collectstatic --settings=leselys.settings_prod --noinput')
    else:
        local('virtenv/bin/python manage.py collectstatic --settings=\'leselys.settings_%s\'' % env)


def virtualenv(command):
    local('source virtenv/bin/activate && ' + command)


@task
def init_virtualenv():
    local('virtualenv virtenv')


@task
def update_messages():
    local('virtenv/bin/python manage.py makemessages -l fr -i virtenv -i venv')


@task
def compile_messages():
    local('virtenv/bin/python manage.py compilemessages')
