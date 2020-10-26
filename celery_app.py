# coding=utf-8
from __future__ import absolute_import

from celery import Celery, bootsteps
from celery.signals import after_task_publish

from kombu import Queue, Exchange

default_queue_name = 'default'
default_exchange_name = 'default'
default_routing_key = 'default'
deadletter_suffix = 'deadletter'
deadletter_queue_name = default_queue_name + "." + deadletter_suffix
deadletter_exchange_name = default_exchange_name + "." + deadletter_suffix
deadletter_routing_key = default_routing_key + "." + deadletter_suffix
# import os
# import sys
# os.chdir('/home/zzy/foo-lib')
# sys.path.append('.')
# print sys.path
# import foo

app = Celery('projq', include=['projq.tasks'])
app.config_from_object('projq.celeryconfig')


class DeclareDLXnDLQ(bootsteps.StartStopStep):
    """
    Celery Bootstep to declare the DL exchange and queues before the worker starts
        processing tasks
    """
    requires = {'celery.worker.components:Pool'}

    def start(self, worker):
        app = worker.app

        # Declare DLX and DLQ
        dlx = Exchange(deadletter_exchange_name, type='direct')

        dead_letter_queue = Queue(deadletter_queue_name, dlx, routing_key=deadletter_routing_key)

        with worker.app.pool.acquire() as conn:
            dead_letter_queue.bind(conn).declare()


@after_task_publish.connect
def task_sent_handler(sender=None, headers=None, body=None, **kwargs):
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    info = headers if 'task' in headers else body
    print('after_task_publish for task id {info[id]}'.format(
        info=info,
    ))


if __name__ == '__main__':
    app.start()
