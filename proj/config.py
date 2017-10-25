from __future__ import absolute_import
from kombu import serialization
#serialization.registry._decoders.pop("application/x-python-serialize")

CELERY_RESULT_BACKEND = 'redis://116.196.114.86:6379/1'
BROKER_URL = 'redis://116.196.114.86:6379/0'

CELERY_ACCEPT_CONTENT=['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
CELERY_ENABLE_UTC = True

