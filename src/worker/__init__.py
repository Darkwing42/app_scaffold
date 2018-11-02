from celery import Celery, current_task
from celery.result import AsyncResult
import os
from src.settings import app_config



worker = Celery('tasks',
		backend=app_config['tasks']['BACKEND_URL'],
		broker=app_config['tasks']['BROKER_URL']
		)


