from abc import ABC


class Schema(ABC):

    def map(self, data: dict):
        pass


class Driver(ABC):
    data: Schema

    def get(self, data_id) -> Schema:
        pass

    def all(self) -> list:
        pass

    def save(self, data_id, data) -> any:
        pass
