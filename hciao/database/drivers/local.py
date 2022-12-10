import copy
import json
import os
from hciao.database.drivers.abstracts import Driver, Schema
from hciao.utils import object
from dataclasses import dataclass


@dataclass()
class LocalSchema(Schema):
    login_id: str | None = None
    checkin_at: str | None = None
    checkout_at: str | None = None
    work_hour: str | None = None

    def map(self, data: dict):
        return object.map_from_dict(self, data)


class LocalDriver(Driver):

    def __init__(self, config: dict):
        super().__init__(config)
        self.path = os.path.join(config['path'], 'local')

    def all(self, data: LocalSchema) -> list[LocalSchema]:
        dir_list = os.listdir(self.path)
        data_list = []
        for filename in dir_list:
            with open(os.path.join(self.path, filename), encoding='utf-8') as f:
                json_dict = json.load(f)

            copy_data = copy.deepcopy(data)
            data_list.append(copy_data.map(json_dict))

        return data_list

    def get(self, data: LocalSchema, date: str = None) -> LocalSchema | None:
        filename = 'local_' + date + '.json'
        try:
            with open(os.path.join(self.path, filename), encoding='utf-8') as f:
                json_dict = json.load(f)
            data = data.map(json_dict)
            data.data_id = date
            return data
        except IOError:
            return None

    def save(self, date_key: str, data: LocalSchema):
        filename = 'local_' + date_key + '.json'
        json_string = object.object_to_json(data)

        with open(os.path.join(self.path, filename), 'w', encoding='utf-8') as f:
            rs = f.write(json_string)

        return rs
