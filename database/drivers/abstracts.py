from abc import ABC
from typing import TypeVar, Generic

T = TypeVar('T')


class Schema(ABC):

    def map(self, data: dict):
        pass


class Driver(ABC, Generic[T]):
    data: Schema
    config: dict

    def __init__(self, config: dict, data_object: T):
        self.config = config
        self.data = data_object

    def get(self, data_id) -> T:
        pass

    def all(self) -> list:
        pass

    def save(self, data_id, data) -> any:
        pass
