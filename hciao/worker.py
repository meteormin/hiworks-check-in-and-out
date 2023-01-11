import os
import time
import subprocess
from datetime import datetime, date
from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from hciao.browser.chrome import Chrome
from hciao.browser.abstracts import Browser
from hciao.logger.log import Log
from hciao.browser.hiworks.elements import Checkin, Checkout, Check
from hciao.browser.login_data import LoginData
from hciao.logger.logger_adapter import LoggerAdapter
from hciao.mailer.abstracts import Mailer
from hciao.schedule.checker import Checker
from hciao.utils import date as util_dt
from hciao.storage.drivers.local import (
    LocalSchema,
    LocalJsonDriver,
    LocalCsvDriver,
    DataStoreEnum,
    sync_local_storages
)
from hciao.storage.drivers.abstracts import Driver
from hciao.mailer.mailer import SimpleMailer


class Worker:
    __constants: dict[str, str]
    __logger: LoggerAdapter
    __data_stores: dict[DataStoreEnum, Driver]
    __mailer: Mailer
    __configs: ConfigParser
    __checker: Checker

    def __init__(self, constants: dict[str, str]):
        """
        Worker Constructor
        :param constants: 상수 값
        :type: constants: Dict[str, str]
        """
        now = datetime.now()

        self.__constants = constants
        self.__configs = self.__config('../settings.ini')

        self.__logger = self.__get_logger('worker')

        self.__data_stores = {
            DataStoreEnum.JSON: self.__get_local_storage(self.__constants['storage']),
            DataStoreEnum.CSV: self.__get_local_csv_storage(self.__constants['storage'])
        }

        data = LocalSchema()
        if self.__data_stores[DataStoreEnum.JSON].get(data, now.strftime('%Y-%m-%d')) is None:
            self.__logger.info('daily pip update...')
            subprocess.run(f"pip3 install -r {constants['base_path']}/../requirements.txt", shell=True)

        self.__mailer = self.__get_mailer(dict(self.__configs['mailer.outlook']))
        self.__checker = Checker(self.__data_stores[DataStoreEnum.JSON])

        self.__logger.debug('start up worker')

    @classmethod
    def __config(cls, file_path: str) -> ConfigParser:
        """
        get config parser
        :param file_path:
        :type file_path: str
        :return: config
        :rtype: ConfigParser
        """
        current_path = os.path.dirname(os.path.abspath(__file__))
        config_parser = ConfigParser()
        config_parser.read(os.path.join(current_path, file_path))
        return config_parser

    @classmethod
    def __get_logger(cls, tag: str) -> LoggerAdapter:
        """
        get logger
        :param tag: tag for logging
        :return: Logger
        :rtype: LoggerAdapter
        """
        return Log.logger(tag)

    @classmethod
    def __get_browser(cls, tag: str, url: str) -> Browser:
        """
        get browser
        :param tag:
        :param url:
        :return: browser
        :rtype: Browser
        """
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        service = Service(ChromeDriverManager().install())

        return Chrome(
            cls.__get_logger(tag),
            webdriver.Chrome(service=service, options=options),
            url
        )

    @classmethod
    def __get_local_storage(cls, path: str) -> Driver:
        """
        get local storage
        :param path:
        :type path: str
        :return: local storage driver
        :rtype: Driver
        """

        return LocalJsonDriver({'path': path})

    @classmethod
    def __get_mailer(cls, mail_config: dict) -> Mailer:
        """
        get mailer
        :param mail_config:
        :return: mailer
        :rtype: Mailer
        """
        return SimpleMailer(
            host=mail_config['url'],
            login_id=mail_config['id'],
            login_pass=mail_config['password']
        )

    @classmethod
    def __get_local_csv_storage(cls, path: str) -> LocalCsvDriver:
        return LocalCsvDriver({'path': path})

    def sync_local_storages(self):
        """
        sync local storages
        :return: int
        """
        self.__logger.info('start sync...')
        save_count = sync_local_storages(list(self.__data_stores.values()))
        self.__logger.info(f'end sync {save_count}')

        return save_count

    def checkin(self, login_id: str, passwd: str) -> int:
        """
        출근하기
        :param login_id:
        :type login_id: str
        :param passwd:
        :type passwd: str
        :return: return 0 is success other value is fail
        :rtype: int
        """
        self.__logger.info('try checkin...')

        if util_dt.is_holidays(date=date.today()):
            self.__logger.info('today is holiday')
            return 1

        conf = self.__configs['hiworks']

        browser = self.__get_browser(self.__logger.prefix + '.checkin', conf['url'])
        data_store = self.__data_stores[DataStoreEnum.JSON]

        if login_id is None or passwd is None:
            login_id = conf['id']
            passwd = conf['password']

        check_time = browser.checkin(LoginData(login_id=login_id, login_pass=passwd), Checkin())

        now = datetime.now()

        data = LocalSchema()
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

    def checkout(self, login_id: str = None, passwd: str = None) -> int:
        """
        퇴근
        :param login_id:
        :param passwd:
        :type login_id: str | None
        :type passwd: str | None
        :return: return 0 is success other value is fail
        :rtype: int
        """
        self.__logger.info('try checkout...')

        if util_dt.is_holidays(date=date.today()):
            self.__logger.info('today is holiday')
            return 1

        conf = self.__configs['hiworks']
        browser = self.__get_browser(self.__logger.prefix + '.checkout', conf['url'])
        data_store = self.__data_stores[DataStoreEnum.JSON]

        if login_id is None or passwd is None:
            login_id = conf['id']
            passwd = conf['password']

        check_time = browser.checkout(LoginData(login_id=login_id, login_pass=passwd), Checkout())

        now = datetime.now()
        data = LocalSchema()
        data = data_store.get(data, now.strftime('%Y-%m-%d'))

        if data is not None and isinstance(data, LocalSchema):
            if check_time is None and check_time == '00:00:00':
                data.checkout_at = now.strftime('%H:%M:%S')
            else:
                data.checkout_at = check_time

            out_time = time.strptime(data.checkout_at, '%H:%M:%S')
            in_time = time.strptime(data.checkin_at, '%H:%M:%S')

            data.work_hour = util_dt.seconds_to_hours(time.mktime(out_time) - time.mktime(in_time))
            data_store.save(now.strftime('%Y-%m-%d'), data)

        return 0

    def check_work_hour(self) -> int:
        """
        check today work hour

        :return:
        :rtype: int
        """
        self.__logger.info('check work hour...')

        now = datetime.now()

        logger = self.__logger
        data_store = self.__data_stores[DataStoreEnum.JSON]

        data = LocalSchema()
        data = data_store.get(data, now.strftime('%Y-%m-%d'))
        if data is None and not isinstance(data, LocalSchema):
            logger.info('not yet checkin')
            return 1

        if data.checkin_at is None:
            logger.info('not yet checkin')
            return 1

        if data.work_hour is not None:
            logger.info(f"already checkout: {data.checkout_at}")
            logger.info(f"work hours: {data.work_hour}")
        else:
            work = self.__checker.get_work_hour_today()
            logger.info(f"work hours: {work.work}")

            if util_dt.hours_to_seconds(work.left) > 0:
                logger.info(f"left hours: {work.left}")
            else:
                logger.info(f"over hours: {work.left}")
        return 0

    def check_and_alert(self) -> int:
        """
        check left time and  when over work time, send alert mail

        :return: 0: success, other value: fail
        :rtype: int
        """
        self.__logger.info('check and alert')

        logger = self.__logger
        conf = self.__configs['hiworks']
        browser = self.__get_browser(self.__logger.prefix + '.check-and-alert', conf['url'])
        data_store = self.__data_stores[DataStoreEnum.JSON]

        now = datetime.now()

        login_id = conf['id']
        passwd = conf['password']

        check_time = browser.check_work(LoginData(login_id, passwd), Check())

        if check_time is not None:
            data = LocalSchema()
            data = data_store.get(data, now.strftime('%Y-%m-%d'))
            if isinstance(data, LocalSchema):
                data.checkin_at = check_time['checkin_at']
                data.checkout_at = check_time['checkout_at']
                data_store.save(now.strftime('%Y-%m-%d'), data)

        data = LocalSchema()
        data = data_store.get(data, now.strftime('%Y-%m-%d'))

        is_checkin = True
        if data is None and not isinstance(data, LocalSchema):
            logger.error('you are not checkin')
            is_checkin = False

        elif data.checkin_at is None:
            logger.debug('not yet checkin')
            is_checkin = False

        hiworks = self.__configs['hiworks']
        mail_config = self.__configs['mailer.outlook']
        mailer = self.__mailer

        if not is_checkin:
            mailer.send(mail_config['id'], f"[Alert] You Don't Checkin...",
                        f"go: {hiworks['url']}")

        if data.work_hour is not None:
            logger.debug(f"already checkout: {data.checkout_at}")
            logger.info(f"work hours: {data.work_hour}")
        else:
            checker = Checker(data_store)
            work = checker.get_work_hour_today()
            logger.info(f"work hours: {work.work}")
            if util_dt.hours_to_seconds(work.left) > 0:
                logger.info(f"left hours: {work.left}")

                if data.checkout_at is not None:
                    logger.debug(f"already checkout: {data.checkout_at}")
            else:
                logger.info(f"over hours: {work.left}")

            if util_dt.hours_to_seconds(work.left) <= 600:
                logger.debug(f"you must checkout!!")

                is_sent = mailer.send(mail_config['mailer.outlook']['id'], '[Alert] You must checkout!!',
                                      f"You must checkout, left {work.left}")
                if is_sent:
                    logger.info("success send mail")
                else:
                    logger.info("fail send mail")
        return 0

    def report_for_month(self, month: int = None, year: int = None) -> int:
        now = datetime.now()
        if year is None:
            year = now.year
        if month is None:
            month = now.month
        if year > now.year:
            raise ValueError("저는 미래를 예측할 수 없어요...")
        elif year == now.year and month > now.month:
            raise ValueError("저는 미래를 예측할 수 없어요...")

        data = LocalSchema()

        driver = self.__data_stores[DataStoreEnum.CSV]

        if isinstance(driver, LocalCsvDriver):
            data_list = driver.get_by_month(data, year, month)
        else:
            self.__logger.error("this instance is not LocalCsvDriver")
            return 1

        self.__logger.info(f"find data in {year}-{month} (count: {len(data_list)})")

        data_path = self.__constants['data']
        local_data_path = os.path.join(data_path, 'local')

        if not os.path.exists(local_data_path):
            self.__logger.info("not exists path...")
            os.mkdir(local_data_path)
            self.__logger.info(f"make dir: {local_data_path}")

        store_path = os.path.join(local_data_path, f"{year}-{month}.csv")

        driver.export_csv(store_path, data_list)

        checker = self.__checker
        checker.set_driver(driver)
        work_hour = checker.get_work_hours_month(month, year)

        mail_config = self.__configs['mailer.outlook']
        mailer = self.__mailer
        mailer.attachment([store_path])
        mailer.send(mail_config['id'], f"[Report] {year}-{month}",
                    f"days: {work_hour.days}, acc: {work_hour.acc}, avg: {work_hour.avg}")

        return 0

    def test(self) -> int:
        """
        just test
        :return: int
        :rtype: int
        """
        self.__logger.info('try test...')

        hiworks = self.__configs['hiworks']
        browser = self.__get_browser(self.__logger.prefix + '.test', hiworks['url'])

        check_time = browser.check_work(
            LoginData(login_id=hiworks['id'], login_pass=hiworks['password']),
            Check()
        )

        if check_time is not None:
            self.__logger.debug(f"checkin_at: {check_time['checkin_at']}")
            self.__logger.debug(f"checkout_at: {check_time['checkout_at']}")

        return 0
