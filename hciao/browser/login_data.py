from dataclasses import dataclass


@dataclass(frozen=True)
class LoginData:
    login_id: str
    login_pass: str
