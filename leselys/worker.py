# -*- coding: utf-8 -*-
import threading
import sys
import time

from leselys import core
from leselys import helpers


class PeriodicTask(threading.Thread):

    def __init__(self, sleep, func, params):
        """ execute func(params) every 'sleep' seconds """
        self.func = func
        self.params = params
        self.sleep = sleep
        threading.Thread.__init__(self, name = "PeriodicExecutor")
        self.setDaemon(1)

    def run(self):
        while True:
            time.sleep(self.sleep)
            apply(self.func, self.params)

def run(config_path):
    core.load_config(config_path)
    core.load_storage()
    core.load_session()

    interval = int(core.config.get('worker', 'interval'))
    retention = int(core.config.get('worker', 'retention'))

    refresh_task = PeriodicTask(10, helpers.refresh_all, [])
    retention_task = PeriodicTask(10, helpers.run_retention, retention)

    refresh_task.run()
    retention_task.run()

def run_old(config_path):
    core.load_config(config_path)
    core.load_storage()
    core.load_session()

    interval = int(core.config.get('worker', 'interval'))
    retention = int(core.config.get('worker', 'retention'))

    def refresh_all():
        print('=> Refresh task')
        helpers.refresh_all()
        #threading.Timer(interval*60, refresh_all).start()
        threading.Timer(10, refresh_all).start()

    def run_retention():
        print('=> Retention task')
        helpers.run_retention(retention)
        #threading.Timer(24*60*60, run_retention, retention).start()
        threading.Timer(10, run_retention, args=[retention]).start()

    refresh_all()
    run_retention()
