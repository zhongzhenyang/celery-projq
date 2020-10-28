# coding=utf-8
from __future__ import absolute_import

from celery import Celery, bootsteps
from celery.signals import after_task_publish, task_success, task_prerun, task_postrun, task_failure

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
def on_after_task_publish(signal=None, sender=None, headers=None, body=None, exchange=None, routing_key=None, **kwargs):
    '''
    after_task_publish signal:<Signal: after_task_publish providing_args={'routing_key', 'exchange', 'body'}>
    after_task_publish sender:add
    after_task_publish header:{'lang': 'py', 'task': 'add', 'id': 'afafd9db-9d34-4280-8012-bdcef1360809', 'shadow': None, 'eta': None, 'expires': None, 'group': None, 'group_index': None, 'retries': 0, 'timelimit': [None, None], 'root_id': 'afafd9db-9d34-4280-8012-bdcef1360809', 'parent_id': None, 'argsrepr': '(2, 4)', 'kwargsrepr': '{}', 'origin': 'gen81941@zzy-ubuntu'}
    after_task_publish body:((2, 4), {}, {'callbacks': None, 'errbacks': None, 'chain': None, 'chord': None})
    after_task_publish exchange:
    after_task_publish routing_key:celery
    after_task_publish kwargs:{}
    task id afafd9db-9d34-4280-8012-bdcef1360809
    '''
    # information about task are located in headers for task messages
    # using the task protocol version 2.
    print('after_task_publish----------------')
    print(f"after_task_publish signal:{signal}")
    print(f"after_task_publish sender:{sender}")
    print(f"after_task_publish header:{headers}")
    print(f"after_task_publish body:{body}")
    print(f"after_task_publish exchange:{exchange}")
    print(f"after_task_publish routing_key:{routing_key}")
    print(f"after_task_publish kwargs:{kwargs}")
    info = headers if 'task' in headers else body
    print('task id {info[id]}'.format(
        info=info,
    ))


@task_prerun.connect
def on_task_prerun(signal=None, sender=None, task_id=None, task=None, **kwargs):
    '''
    task_prerun signal:<Signal: task_prerun providing_args={'task', 'kwargs', 'task_id', 'args'}>
    task_prerun sender:<@task: add of projq at 0x7fb3cbc7e400>
    task_prerun task_id:88cab53d-1882-41c7-b700-9777c0d4ce26
    task_prerun task:<@task: add of projq at 0x7fb3cbc7e400>
    task_prerun kwargs:{'args': [10, 10], 'kwargs': {}}
    '''
    print('task_prerun----------------')
    print(f"task_prerun signal:{signal}")
    print(f"task_prerun sender:{sender}")
    print(f"task_prerun task_id:{task_id}")
    print(f"task_prerun task:{task}")
    print(f"task_prerun kwargs:{kwargs}")


@task_postrun.connect
def on_task_postrun(signal=None, sender=None, task_id=None, task=None, retval=None, state=None, **kwargs):
    '''
    task_postrun signal:<Signal: task_postrun providing_args={'task_id', 'kwargs', 'args', 'retval', 'task'}>
    task_postrun sender:<@task: add of projq at 0x7fb3cbc7e400>
    task_postrun task_id:88cab53d-1882-41c7-b700-9777c0d4ce26
    task_postrun task:<@task: add of projq at 0x7fb3cbc7e400>
    task_postrun kwargs:{'args': [10, 10], 'kwargs': {}}
    task_postrun retval:20
    task_postrun state:SUCCESS
    '''
    print('task_postrun----------------')
    print(f"task_postrun signal:{signal}")
    print(f"task_postrun sender:{sender}")
    print(f"task_postrun task_id:{task_id}")
    print(f"task_postrun task:{task}")
    print(f"task_postrun kwargs:{kwargs}")
    print(f"task_postrun retval:{retval}")
    print(f"task_postrun state:{state}")


@task_success.connect
def on_task_success(signal=None, sender=None, result=None, **kwargs):
    '''
    task_success signal:<Signal: task_success providing_args={'result'}>
    task_success sender:<@task: add of projq at 0x7fb91fb98400>
    task_success result:63
     task_success kwargs:{}
    '''
    print('task_success-------------------')
    print(f"task_success signal:{signal}")
    print(f"task_success sender:{sender}")
    print(f"task_success result:{result}")
    print(f"task_success kwargs:{kwargs}")


@task_failure.connect
def on_task_failure(signal=None, sender=None, task_id=None, exception=None, traceback=None, einfo=None, **kwargs):
    '''

    task_failure signal:<Signal: task_failure providing_args={'args', 'kwargs', 'exception', 'einfo', 'task_id', 'traceback'}>
    task_failure sender:<@task: add of projq at 0x7f9c7f0c0400>
    task_failure task_id:db7be10e-b957-46e0-a466-5206a42fc7cf
    task_failure exception:my error
    task_failure traceback:<traceback object at 0x7f9c7eabf400>
    task_failure einfo:Traceback (most recent call last):
      File "/home/zzy/.pyenv/versions/3.8.5/envs/celery-env/lib/python3.8/site-packages/celery/app/trace.py", line 409, in trace_task
        R = retval = fun(*args, **kwargs)
      File "/home/zzy/.pyenv/versions/3.8.5/envs/celery-env/lib/python3.8/site-packages/celery/app/trace.py", line 701, in __protected_call__
        return self.run(*args, **kwargs)
      File "/home/zzy/works/py-works/projects/celery-projq/tasks.py", line 30, in add
        raise RuntimeError("my error")
    RuntimeError: my error
    task_failure kwargs:{'args': [1, 61], 'kwargs': {}}
    '''
    print('task_failure-------------------')
    print(f"task_failure signal:{signal}")
    print(f"task_failure sender:{sender}")
    print(f"task_failure task_id:{task_id}")
    print(f"task_failure exception:{exception}")
    print(f"task_failure traceback:{traceback}")
    print(f"task_failure einfo:{einfo}")
    print(f"task_failure kwargs:{kwargs}")


if __name__ == '__main__':
    app.start()
