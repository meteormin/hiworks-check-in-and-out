from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class Schema(ABC):

    @abstractmethod
    def map(self, data: dict):
        pass


class Driver(ABC, Generic[T]):
    data: Schema
    config: dict

    def __init__(self, config: dict, data_object: T):
        self.config = config
        self.data = data_object

    @abstractmethod
    def get(self, data_id) -> T:
        pass

    @abstractmethod
    def all(self) -> list:
        pass

    @abstractmethod
    def save(self, data_id, data) -> any:
        pass
