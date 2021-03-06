# coding=utf-8
from __future__ import absolute_import

from celery.utils.log import get_task_logger

from .celery_app import app
import functools
import time

task_registry = {}
logger = get_task_logger(__name__)


def register(category, name):
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, **kwargs):
            return f(*args, **kwargs)

        task_registry[category + ':' + name] = f
        return wrapped

    return wrapper


@app.task(name='add')
# @register('foo', 'add')
# @app.task
def add(x, y):
    if x == 1:
        raise RuntimeError("my error")
    return x + y


@app.task(name="add3")
def add3(a, b=10, c=20):
    return a + b + c


@app.task(name='foo')
def foo(x):
    print("foo:" + str(x))


@app.task
def bar(x):
    print("bar:" + str(x))


@app.task(countdown=3)
def show_info(x):
    print(x)


def create_x():
    print("create x")
    return 20
