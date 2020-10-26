# coding=utf-8
from __future__ import absolute_import

from celery import Celery, bootsteps
from celery.signals import after_task_publish, task_success

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

app = Celery('projq', include=['celery-projq.tasks'])
app.config_from_object('celery-projq.celeryconfig')


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
def on_after_task_publish(sender=None, headers=None, body=None, **kwargs):
    '''
    after_task_publish sender:add
    after_task_publish header:{'lang': 'py', 'task': 'add', 'id': '71e991fc-06d8-4720-9ad2-a8066bb0b44a', 'shadow': None, 'eta': None, 'expires': None, 'group': None, 'group_index': None, 'retries': 0, 'timelimit': [None, None], 'root_id': '71e991fc-06d8-4720-9ad2-a8066bb0b44a', 'parent_id': None, 'argsrepr': '(2, 2)', 'kwargsrepr': '{}', 'origin': 'gen30710@zzy-ubuntu'}
    after_task_publish body:((2, 2), {}, {'callbacks': None, 'errbacks': None, 'chain': None, 'chord': None})
    after_task_publish kwargs:{'signal': <Signal: after_task_publish providing_args={'exchange', 'body', 'routing_key'}>, 'exchange': '', 'routing_key': 'celery'}
    task id 71e991fc-06d8-4720-9ad2-a8066bb0b44a
    '''
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    print('after_task_publish----------------')
    print(f"after_task_publish sender:{sender}")
    print(f"after_task_publish header:{headers}")
    print(f"after_task_publish body:{body}")
    print(f"after_task_publish kwargs:{kwargs}")
    info = headers if 'task' in headers else body
    print('task id {info[id]}'.format(
        info=info,
    ))


@task_success.connect
def on_task_success(sender=None, result=None, **kwargs):
    '''
    task_success sender:<@task: add of projq at 0x7f3925602a30>
    task_success result:4
    task_success kwargs:{'signal': <Signal: task_success providing_args={'result'}>}
    '''
    print('task_success-------------------')
    print(f"task_success sender:{sender}")
    print(f"task_success result:{result}")
    print(f"task_success kwargs:{kwargs}")


if __name__ == '__main__':
    app.start()
