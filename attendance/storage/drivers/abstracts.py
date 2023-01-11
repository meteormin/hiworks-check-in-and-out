from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')


@dataclass()
class Schema(ABC):
    data_id: str | int = None

    @abstractmethod
    def map(self, data: dict):
        pass


class Driver(ABC, Generic[T]):
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
