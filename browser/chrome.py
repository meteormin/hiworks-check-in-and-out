from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from browser.login_data import LoginData
from logger.logger_adapter import LoggerAdapter
from browser.hiworks.elements import Check, Checkin, Checkout
from browser.hiworks.elements import LoginElement
import os
from time import sleep


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

    def _check(self, driver: WebDriver, check_data: Check) -> bool:
        if isinstance(check_data, Checkin):
            index = 0
        elif isinstance(check_data, Checkout):
            index = 1
        else:
            return False

        driver.implicitly_wait(2)
        sleep(0.3)

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

            self.logger.debug("info: page is ready")
        except TimeoutException:
            self.logger.error('timeout 5s')
        sleep(0.3)

        try:
            if element is not None:
                element_detail = driver.find_element(By.CSS_SELECTOR, check_data.detail)
                element_check = element_detail.find_elements(By.CSS_SELECTOR, check_data.check_btn)[index]
                element_text = element_check.find_element(By.CSS_SELECTOR, check_data.check_text_div)
                if element_text.get_attribute('textContent') == check_data.check_text_content:
                    self.logger.debug(element_text.get_attribute('textContent'))
                    self.logger.debug(element_check.tag_name)
                    element_check.click()
                    if index == 1:
                        alert = driver.switch_to.alert
                        self.logger.debug(f"alert: {alert.text}")
                        sleep(0.3)
                        alert.accept()
                    sleep(1)
                else:
                    self.logger.debug(element_check.get_attribute('innerHTML'))
                    self.logger.debug(element_check.tag_name)
        except NoSuchElementException as e:
            self.logger.error(e)

        return True

    def checkin(self, login_data: LoginData, checkin_data: Checkin):
        driver = self._login(login_data.login_id, login_data.login_pass)
        return self._check(driver, checkin_data)

    def checkout(self, login_data: LoginData, checkout_data: Checkout):
        driver = self._login(login_data.login_id, login_data.login_pass)
        return self._check(driver, checkout_data)
