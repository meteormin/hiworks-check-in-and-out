from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class Schema(ABC):
    data_id: str | int

    @abstractmethod
    def map(self, data: dict):
        pass


class Driver(ABC, Generic[T]):
    config: dict

    def __init__(self, config: dict):
        self.config = config

    @abstractmethod
    def get(self, data: T, data_id: str | int = None) -> T:
        pass

    @abstractmethod
    def all(self, data: T) -> list[T]:
        pass

    @abstractmethod
    def save(self, data_id, data) -> any:
        pass
