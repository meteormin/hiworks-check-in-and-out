import os
from datetime import datetime
from time import sleep
from typing import Union
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from logger.logger_adapter import LoggerAdapter
from browser.login_data import LoginData
from browser.hiworks.elements import Check, Checkin, Checkout
from browser.hiworks.elements import LoginElement


class Chrome:

    def __init__(self, logger: LoggerAdapter, driver: WebDriver, url: str):
        current_path = os.path.dirname(os.path.abspath(__file__))
        self.driver = driver
        self.logger = logger
        self.url = url

    def _login(self, _id: str, passwd: str) -> WebDriver:
        login_data = LoginElement()
        self.driver.get(self.url)
        element_id = self.driver.find_element(By.CSS_SELECTOR, login_data.input_id)
        element_pass = self.driver.find_element(By.CSS_SELECTOR, login_data.input_pass)
        element_login_btn = self.driver.find_element(By.CSS_SELECTOR, login_data.login_btn)

        try:
            WebDriverWait(self.driver, 5).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, login_data.input_id))
            )

            self.logger.debug("info: page is ready")
        except TimeoutException:
            self.logger.error('timeout 5s')

        try:
            element_id.send_keys(_id)
        except NoSuchElementException:
            self.logger.error(f'cant not found element by id({login_data.input_id})')

        try:
            element_pass.send_keys(passwd)
        except NoSuchElementException:
            self.logger.error(f'can not found element by id({login_data.input_pass})')

        try:
            element_login_btn.click()
        except NoSuchElementException:
            self.logger.error(f'can not found element by className({login_data.login_btn})')

        self.logger.info('process: login...')

        try:
            WebDriverWait(self.driver, 5).until(
                ec.presence_of_all_elements_located
            )
            self.logger.info("ready for start parse")
        except TimeoutException:
            self.logger.error("timeout 5s")

        self.logger.info('success: login')

        return self.driver

    def _open_div(self, driver: WebDriver, check_data: Check):
        element = None

        try:
            WebDriverWait(driver, 5).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, check_data.wrap_class))
            )

            self.logger.debug("info: page is ready")
        except TimeoutException:
            self.logger.error('timeout 5s')
        sleep(0.3)

        try:
            element = driver.find_element(By.CSS_SELECTOR, check_data.wrap_class)
            open_div_btn = element.find_element(By.CSS_SELECTOR, check_data.open_div_btn)
            open_div_btn.click()

            self.logger.debug(f'open div {open_div_btn.tag_name}')
        except NoSuchElementException as e:
            self.logger.error(f'not found element by css selector {check_data.wrap_class}')
            self.logger.error(e)

        try:
            WebDriverWait(driver, 5).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, check_data.detail))
            )

            self.logger.debug("page is ready")
        except TimeoutException:
            self.logger.error('timeout 5s')
        sleep(0.3)

        return element

    def _check(self, driver: WebDriver, check_data: Check) -> Union[WebElement, None]:
        if isinstance(check_data, Checkin):
            index = 0
        elif isinstance(check_data, Checkout):
            index = 1
        elif isinstance(check_data, Check):
            index = None
        else:
            return None

        driver.implicitly_wait(2)
        sleep(0.3)

        element = self._open_div(driver, check_data)

        try:
            if element is not None:
                element_detail = driver.find_element(By.CSS_SELECTOR, check_data.detail)

                return element_detail
        except NoSuchElementException as e:
            self.logger.error(e)
            return None

    def _check_btn_click(self, check_btn: WebElement, check_data: Check) -> bool:
        element_text = check_btn.find_element(By.CSS_SELECTOR, check_data.check_text_div)
        try:
            if element_text.get_attribute('textContent') == check_data.check_text_content:
                self.logger.debug(element_text.get_attribute('textContent'))
                self.logger.debug(check_btn.tag_name)
                check_btn.click()
                sleep(0.3)

            else:
                self.logger.debug(check_btn.get_attribute('innerHTML'))
                self.logger.debug(check_btn.tag_name)

            return True
        except NoSuchElementException as e:
            self.logger.error(e)
            return False

    def checkin(self, login_data: LoginData, checkin_data: Checkin):
        driver = self._login(login_data.login_id, login_data.login_pass)
        element_detail = self._check(driver, checkin_data)
        check_time = None
        if element_detail is not None:
            try:
                element_check = element_detail.find_elements(By.CSS_SELECTOR, checkin_data.check_btn)[
                    checkin_data.index]

                if self._check_btn_click(element_check, checkin_data):
                    element_check_time = element_detail.find_elements(By.CSS_SELECTOR, checkin_data.check_time_div)
                    check_time = element_check_time[checkin_data.index].get_attribute('innerHTML')
                    check_time = check_time.strip()
                    self.logger.debug(check_time)
                else:
                    self.logger.error('failed click: not found check btn')

            except NoSuchElementException as e:
                self.logger.error(e)

            sleep(1)

        return check_time

    def checkout(self, login_data: LoginData, checkout_data: Checkout):
        driver = self._login(login_data.login_id, login_data.login_pass)
        element_detail = self._check(driver, checkout_data)
        check_time = None
        if element_detail is not None:
            try:
                element_check = element_detail.find_elements(By.CSS_SELECTOR, checkout_data.check_btn)[
                    checkout_data.index]

                if self._check_btn_click(element_check, checkout_data):
                    alert = driver.switch_to.alert
                    self.logger.debug(f"alert: {alert.text}")
                    alert.accept()
                    check_time = datetime.now().strftime("%H:%M:%S")
                else:
                    self.logger.error('failed click: not found check btn')

            except NoSuchElementException as e:
                self.logger.error(e)

            sleep(1)

        return check_time

    def check_work(self, login_data: LoginData, check_data: Check):
        driver = self._login(login_data.login_id, login_data.login_pass)
        element_detail = self._check(driver, check_data)
        check_work_time = {'checkin_at': None, 'checkout_at': None}

        if element_detail is not None:
            try:
                element_checkin = element_detail.find_elements(By.CSS_SELECTOR, check_data.check_btn)[0]
                element_checkout = element_detail.find_elements(By.CSS_SELECTOR, check_data.check_btn)[1]

                if element_checkin:
                    element_check_time = element_detail.find_elements(By.CSS_SELECTOR, check_data.check_time_div)
                    check_time = element_check_time[0].get_attribute('innerHTML')
                    checkin_time = check_time.strip()
                    self.logger.debug(checkin_time)

                    if checkin_time == '00:00:00':
                        checkin_time = None

                    check_work_time['checkin_at'] = checkin_time

                if element_checkout:
                    element_check_time = element_detail.find_elements(By.CSS_SELECTOR, check_data.check_time_div)
                    check_time = element_check_time[1].get_attribute('innerHTML')
                    checkout_time = check_time.strip()
                    self.logger.debug(checkout_time)

                    if checkout_time == '00:00:00':
                        checkout_time = None

                    check_work_time['checkout_at'] = checkout_time

            except NoSuchElementException as e:
                self.logger.error(e)

            return check_work_time
        return None
