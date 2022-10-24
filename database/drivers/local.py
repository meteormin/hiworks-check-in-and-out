import json
import os
from typing import Union
from utils import object


class LocalSchema:
    login_id: str
    checkin_at: Union[str, None]
    checkout_at: Union[str, None]
    work_hour: int = 0

    def __init__(self, json_dict: dict = None):
        if json_dict is None:
            return

        if 'login_id' in json_dict:
            self.login_id = json_dict['login_id']

        if 'checkin_at' in json_dict:
            self.checkin_at = json_dict['checkin_at']

        if 'checkout_at' in json_dict:
            self.checkout_at = json_dict['checkout_at']

        if 'work_hour' in json_dict:
            self.work_hour = json_dict['work_hour']

    def map(self, data: dict):
        if 'login_id' in data:
            self.login_id = data['login_id']

        if 'checkin_at' in data:
            self.checkin_at = data['checkin_at']

        if 'checkout_at' in data:
            self.checkout_at = data['checkout_at']

        if 'work_hour' in data:
            self.work_hour = data['work_hour']
        return self


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
