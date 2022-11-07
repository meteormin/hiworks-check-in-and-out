import os
import time
import subprocess
from typing import Dict, Union
from datetime import datetime, date
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from browser.chrome import Chrome
from logger.log import Log
from browser.hiworks.elements import Checkin, Checkout, Check
from browser.login_data import LoginData
from schedule.checker import Checker
from utils.date import is_holidays, seconds_to_hours
from database.drivers.local import LocalSchema, LocalDriver
from mailer.mailer import SimpleMailer


class Worker:
    __constants: Dict[str, str]

    def __init__(self, constants: Dict[str, str]):
        self.__constants = constants
        logger = self.get_logger('worker')
        now = datetime.now()
        data_store = self.get_local_storage(self.__constants['database'])

        logger.debug('start up worker')

        if data_store.get(now.strftime('%Y-%m-%d')) is None:
            logger.info('daily pip update...')
            subprocess.run(f"pip3 install -r {constants['base']}/requirements.txt", shell=True)

    @classmethod
    def config(cls, file_path: str):
        current_path = os.path.dirname(os.path.abspath(__file__))
        config_parser = ConfigParser()
        config_parser.read(os.path.join(current_path, file_path))
        return config_parser

    @classmethod
    def get_logger(cls, tag: str):
        return Log.logger(tag)

    @classmethod
    def get_browser(cls, tag: str, url: str):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        service = Service(ChromeDriverManager().install())

        return Chrome(
            cls.get_logger(tag),
            webdriver.Chrome(service=service, options=options),
            url
        )

    @classmethod
    def get_local_storage(cls, path: str) -> LocalDriver:
        data = LocalSchema()
        return LocalDriver(path, data)

    @classmethod
    def get_mailer(cls, mail_config: dict) -> SimpleMailer:
        return SimpleMailer(
            host=mail_config['outlook']['url'],
            login_id=mail_config['outlook']['id'],
            login_pass=mail_config['outlook']['password']
        )

    def checkin(self, login_id: str, passwd: str):
        logger = self.get_logger('checkin')

        if is_holidays(date=date.today()):
            logger.info('today is holiday')
            return 1
        conf = self.config('hiworks.ini')
        if login_id is None or passwd is None:
            login_id = conf['default']['id']
            passwd = conf['default']['password']

        url = conf['default']['url']

        browser = self.get_browser('checkin', url)

        check_time = browser.checkin(LoginData(login_id=login_id, login_pass=passwd), Checkin())

        now = datetime.now()
        data_store = self.get_local_storage(self.__constants['database'])

        data = data_store.data
        data.login_id = login_id
        data.checkout_at = None
        data.work_hour = None

        if check_time is None and check_time == '00:00:00':
            data.checkin_at = now.strftime('%Y-%m-%d')
        else:
            data.checkin_at = check_time

        if data_store.save(now.strftime('%Y-%m-%d'), data):
            return 0

        return 1

    def checkout(self, login_id: str = None, passwd: str = None):
        if is_holidays(date=date.today()):
            return 1

        conf = self.config('hiworks.ini')
        if login_id is None or passwd is None:
            login_id = conf['default']['id']
            passwd = conf['default']['password']

        url = conf['default']['url']

        browser = self.get_browser('checkout', url)
        check_time = browser.checkout(LoginData(login_id=login_id, login_pass=passwd), Checkout())

        data_store = self.get_local_storage(self.__constants['database'])

        now = datetime.now()
        data = data_store.get(now.strftime('%Y-%m-%d'))

        if data is not None:
            if check_time is None and check_time == '00:00:00':
                data.checkout_at = now.strftime('%H:%M:%S')
            else:
                data.checkout_at = check_time

            out_time = time.strptime(data.checkout_at, '%H:%M:%S')
            in_time = time.strptime(data.checkin_at, '%H:%M:%S')

            data.work_hour = seconds_to_hours(time.mktime(out_time) - time.mktime(in_time))
            data_store.save(now.strftime('%Y-%m-%d'), data)

        return 0

    def check_work_hour(self):
        now = datetime.now()

        data_store = self.get_local_storage(self.__constants['database'])
        data = data_store.get(now.strftime('%Y-%m-%d'))
        logger = self.get_logger('check-work-hour')

        if data.checkin_at is None:
            logger.info('not yet checkin')
            return 1

        if data.work_hour is not None:
            logger.info(f"already checkout: {data.checkout_at}")
            logger.info(f"work hours: {data.work_hour}")
        else:
            checker = Checker(data_store)
            work = checker.get_work_hour_today()
            logger.info(f"work hours: {seconds_to_hours(work['work'])}")

            if work['left'] > 0:
                logger.info(f"left hours: {seconds_to_hours(work['left'])}")
            else:
                logger.info(f"over hours: {seconds_to_hours(work['left'])}")
        return 0

    def check_and_alert(self):
        logger = self.get_logger('check-and-alert')

        now = datetime.now()
        conf = self.config('hiworks.ini')

        login_id = conf['default']['id']
        passwd = conf['default']['password']
        url = conf['default']['url']

        browser = self.get_browser('check-and-alert', url)
        check_time = browser.check_work(LoginData(login_id, passwd), Check())

        data_store = self.get_local_storage(self.__constants['database'])

        if check_time is not None:
            data_store.update_work_time(now.strftime('%Y-%m-%d'), check_time)

        data = data_store.get(now.strftime('%Y-%m-%d'))

        if data is None:
            logger.error('you are not checkin')
            return 1

        mail_config = self.config('mailer.ini')
        mailer = self.get_mailer(mail_config)

        if data.checkin_at is None:
            logger.debug('not yet checkin')
            hiworks = self.config('hiworks.ini')

            mailer.send(mail_config['outlook']['id'], f"[Alert] You Don't Checkin...", f"go: {hiworks['url']}")
            return 1

        if data.work_hour is not None:
            logger.debug(f"already checkout: {data.checkout_at}")
            logger.info(f"work hours: {data.work_hour}")
        else:
            checker = Checker(data_store)
            work = checker.get_work_hour_today()
            logger.info(f"work hours: {seconds_to_hours(work['work'])}")
            if work['left'] > 0:
                logger.info(f"left hours: {seconds_to_hours(work['left'])}")

                if data.checkout_at is not None:
                    logger.debug(f"already checkout: {data.checkout_at}")
            else:
                logger.info(f"over hours: {seconds_to_hours(work['left'])}")

            if work['left'] <= 600:
                logger.debug(f"you must checkout!!")

                mailer.send(mail_config['outlook']['id'], '[Alert] You must checkout!!',
                            f"You must checkout, left {seconds_to_hours(work['left'])}")

        return 0
