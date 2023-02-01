from abc import ABC, abstractmethod


class Mailer(ABC):

    @abstractmethod
    def login(self, login_id: str, login_pass: str):
        pass

    @abstractmethod
    def attachment(self, file_path: list):
        pass

    @abstractmethod
    def send(self, to: str, subject: str, msg: str):
        pass
