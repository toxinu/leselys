# -*- coding: utf-8 -*-
from __future__ import absolute_import

import sys
from celery import Celery
from leselys import core
from leselys.helpers import refresh_all
from datetime import timedelta


def run(config_path, args):
	celery = Celery('tasks', broker='mongodb://localhost:27017/leselys')

	args.append('-B')
	core.load_config(config_path)
	core.load_storage()
	core.load_session()

	interval = core.config.get('worker', 'interval')

	@celery.task
	def refresh_all():
		helper.refresh_all()

	celery.conf.CELERYBEAT_SCHEDULE = {
	'refresh-job': {
    	'task': 'leselys.worker.refresh_all',
    	'schedule': timedelta(minutes=int(interval))
    	},
	}
	celery.conf.INSTALLED_APPS = ('tasks.refresh_all',)

	print('Args: %s' % ' '.join(args))
	celery.start(args)
