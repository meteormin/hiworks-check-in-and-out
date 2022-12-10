from abc import ABC, abstractmethod


class Mailer(ABC):

    @abstractmethod
    def login(self, login_id: str, login_pass: str):
        pass

    @abstractmethod
    def send(self, to: str, subject: str, msg: str) -> bool:
        pass
