from abc import ABC, abstractmethod
from typing import Optional, Dict
from browser.hiworks.elements import Check
from browser.login_data import LoginData


class Browser(ABC):
    @abstractmethod
    def checkin(self, login_data: LoginData, check_data: Check) -> Optional[str]:
        pass

    @abstractmethod
    def checkout(self, login_data: LoginData, check_data: Check) -> Optional[str]:
        pass

    @abstractmethod
    def check_work(self, login_data: LoginData, check_data: Check) -> Optional[Dict[str, Optional[str]]]:
        pass
