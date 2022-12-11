import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

PATH = {
    'base_path': BASE_PATH,
    'config': os.path.join(BASE_PATH, 'config'),
    'browser': os.path.join(BASE_PATH, 'browser'),
    'storage': os.path.join(BASE_PATH, 'storage'),
    'logger': os.path.join(BASE_PATH, 'logger'),
    'logs': os.path.join(BASE_PATH, '../logs'),
    'schedule': os.path.join(BASE_PATH, 'schedule'),
    'utils': os.path.join(BASE_PATH, 'utils'),
    'data': os.path.join(BASE_PATH, '../data'),
}

WORK_HOURS = 9
TIMEZONE = 'Asia/Seoul'
