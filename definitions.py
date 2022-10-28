import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

PATH = {
    'browser': os.path.join(BASE_PATH, 'browser'),
    'database': os.path.join(BASE_PATH, 'database'),
    'logger': os.path.join(BASE_PATH, 'logger'),
    'logs': os.path.join(BASE_PATH, 'logs'),
    'schedule': os.path.join(BASE_PATH, 'schedule'),
    'utils': os.path.join(BASE_PATH, 'utils'),
}

WORK_HOURS = 9
