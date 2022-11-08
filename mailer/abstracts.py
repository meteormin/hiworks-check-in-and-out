from abc import ABC


class Mailer(ABC):

    def login(self, login_id: str, login_pass: str):
        pass

    def send(self, to: str, subject: str, msg: str) -> bool:
        pass
