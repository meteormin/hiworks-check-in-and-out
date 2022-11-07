import json
import os
from typing import Union
from utils import object
from dataclasses import dataclass


@dataclass()
class LocalSchema:
    login_id: Union[str, None] = None
    checkin_at: Union[str, None] = None
    checkout_at: Union[str, None] = None
    work_hour: Union[str, None] = None

    def map(self, data: dict):
        return object.map_from_dict(self, data)


class LocalDriver:

    def __init__(self, base_path: str, data_object: LocalSchema):
        self.path = os.path.join(base_path, 'local')
        self.data = data_object

    def all(self):
        dir_list = os.listdir(self.path)
        data_dict = {}
        for filename in dir_list:
            with open(os.path.join(self.path, filename), encoding='utf-8') as f:
                json_dict = json.load(f)
            data_dict[filename] = self.data.map(json_dict)
        return data_dict

    def get(self, date: str) -> Union[LocalSchema, None]:
        filename = 'local_' + date + '.json'
        try:
            with open(os.path.join(self.path, filename), encoding='utf-8') as f:
                json_dict = json.load(f)
            return self.data.map(json_dict)
        except IOError:
            return None

    def save(self, date_key: str, data: LocalSchema):
        filename = 'local_' + date_key + '.json'
        json_string = object.object_to_json(data)

        with open(os.path.join(self.path, filename), 'w', encoding='utf-8') as f:
            rs = f.write(json_string)

        return rs
