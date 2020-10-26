# coding=utf-8
from __future__ import absolute_import

from kombu import Queue

default_queue_name = 'default'
default_exchange_name = 'default'
default_routing_key = 'default'
deadletter_suffix = 'deadletter'
deadletter_queue_name = default_queue_name + "." + deadletter_suffix
deadletter_exchange_name = default_exchange_name + "." + deadletter_suffix
deadletter_routing_key = default_routing_key + "." + deadletter_suffix

BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24
CELERY_ACCEPT_CONTENT = ['json']

#
# CELERY_QUEUES = (
#     Queue('default', routing_key='tasks.#'),
#     Queue('foo', routing_key='tasks.#'),
#     Queue('add', routing_key='tasks.#', queue_arguments={
#         'x-dead-letter-exchange': deadletter_exchange_name,
#         'x-dead-letter-routing-key': deadletter_routing_key
#     }),
#     # Queue('web_tasks', routing_key='web.#'),
#     # Queue('foo_queue', routing_key="task.foo")
# )

# CELERY_DEFAULT_EXCHANGE = 'tasks'
# CELERY_DEFAULT_EXCHANGE_TYPE = 'topic'
# CELERY_DEFAULT_ROUTING_KEY = 'task.default'
#
# CELERY_ROUTES = {
#     'projq.tasks.add': {
#         'queue': 'add',
#
#     },
#     'projq.tasks.foo': {
#         'queue': 'foo',
#
#     }
# }



