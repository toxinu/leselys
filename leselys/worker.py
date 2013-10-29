# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys

from celery import Celery
from leselys import core
from leselys import helpers
from datetime import timedelta


def run(config_path, args):
    args.append('-B')
    args.append('-l')
    args.append('INFO')
    core.load_config(config_path)
    core.load_storage()
    core.load_session()

    broker = core.config.get('worker', 'broker')
    interval = core.config.get('worker', 'interval')
    retention = core.config.get('worker', 'retention')
    story_before_retention = core.config.get('worker', 'story_before_retention')

    celery = Celery('tasks', broker=broker)

    @celery.task
    def refresh_all():
        helpers.refresh_all()

    @celery.task
    def run_retention(delta):
        helpers.run_retention(delta)

    celery.conf.CELERYBEAT_SCHEDULE = {
        'refresh-job': {
            'task': 'leselys.worker.refresh_all',
            'schedule': timedelta(minutes=int(interval))
        },
        'retention-job': {
            'task': 'leselys.worker.run_retention',
            'schedule': timedelta(days=1),
            'args': (int(retention), int(story_before_retention))
        }
    }
    celery.conf.INSTALLED_APPS = ('tasks.refresh_all', 'tasks.run_retention')

    print('Args: %s' % ' '.join(args))
    celery.start(args)
