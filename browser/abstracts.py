from abc import ABC
from typing import Union, Dict
from browser.hiworks.elements import Check
from browser.login_data import LoginData


class Browser(ABC):

    def checkin(self, login_data: LoginData, check_data: Check):
        pass

    def checkout(self, login_data: LoginData, check_data: Check):
        pass

    def check_work(self, login_data: LoginData, check_data: Check) -> Union[Dict[str, str], None]:
        pass

    def test(self, login_data: LoginData, check_data: Check):
        pass
