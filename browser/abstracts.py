"""
about browser abstracts
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict
from browser.hiworks.elements import Check
from browser.login_data import LoginData


class Browser(ABC):
    """
    Abstract Browser class
    """

    @abstractmethod
    def checkin(self, login_data: LoginData, check_data: Check) -> Optional[str]:
        """

        :param login_data:
        :param check_data:
        :return:
        """

    @abstractmethod
    def checkout(self, login_data: LoginData, check_data: Check) -> Optional[str]:
        """

        :param login_data:
        :param check_data:
        :return:
        """

    @abstractmethod
    def check_work(self, login_data: LoginData, check_data: Check) -> Optional[Dict[str, Optional[str]]]:
        """

        :param login_data:
        :param check_data:
        :return:
        """
