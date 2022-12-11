import json
from typing import TypeVar, Generic

T = TypeVar('T')


def object_to_json(obj: object):
    return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4, ensure_ascii=False)


def map_from_dict(obj: T, data: dict) -> T:
    for k, v in data.items():
        if k in obj.__dict__.keys():
            obj.__setattr__(k, v)
    return obj
