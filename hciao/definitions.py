import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

PATH = {
    'base_path': BASE_PATH,
    'config': os.path.join(BASE_PATH, 'config'),
    'browser': os.path.join(BASE_PATH, 'browser'),
    'database': os.path.join(BASE_PATH, 'database'),
    'logger': os.path.join(BASE_PATH, 'logger'),
    'logs': os.path.join(BASE_PATH, '../logs'),
    'schedule': os.path.join(BASE_PATH, 'schedule'),
    'utils': os.path.join(BASE_PATH, 'utils'),
}

WORK_HOURS = 9
TIMEZONE = 'Asia/Seoul'
