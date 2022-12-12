import copy
import json
import os
import pandas
import dfquery
from natsort import natsorted
from enum import Enum
from dataclasses import dataclass
from hciao.storage.drivers.abstracts import Driver, Schema, T
from hciao.utils import object


def sync_local_storages(data_stores: list[Driver]):
    data_list = []
    for store in data_stores:
        data_list.append(store.all(LocalSchema()))

    max_idx = 0

    for idx, data in enumerate(data_list):
        if len(data) > len(data_list[max_idx]):
            max_idx = idx

    save_count = 0
    for idx, store in enumerate(data_stores):
        if idx == max_idx:
            continue
        for data in data_list[max_idx]:
            save_count += 1
            store.save(data.data_id, data)
    return save_count


def make_local_dir(path: str):
    local_path = os.path.join(path, 'local')

    if os.path.exists(local_path):
        return

    os.mkdir(local_path)


class DataStoreEnum(str, Enum):
    JSON = 'json'
    CSV = 'csv'

    def __str__(self):
        return self.value


@dataclass()
class LocalSchema(Schema):
    login_id: str | None = None
    checkin_at: str | None = None
    checkout_at: str | None = None
    work_hour: str | None = None

    def map(self, data: dict):
        return object.map_from_dict(self, data)


class LocalJsonDriver(Driver):
    data_list: list[LocalSchema] = []

    def __init__(self, config: dict):
        super().__init__(config)
        make_local_dir(config['path'])

        self.path = os.path.join(config['path'], 'local')
        self.data_list = self.all(LocalSchema())

    def all(self, data: LocalSchema) -> list[LocalSchema]:
        if self.data_list is not None and len(self.data_list) != 0:
            return self.data_list

        dir_list = natsorted(os.listdir(self.path))
        data_list = []
        for filename in dir_list:
            basename = os.path.basename(filename).split('_')[-1]
            [data_id, ext] = os.path.splitext(basename)

            if ext == '.json':
                with open(os.path.join(self.path, filename), encoding='utf-8') as f:
                    json_dict = json.load(f)

                copy_data = copy.deepcopy(data)
                copy_data.data_id = data_id
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
        data.data_id = date_key

        exists = None
        for i, exists_data in enumerate(self.data_list):
            if exists_data.data_id == date_key:
                exists = {'index': i, 'data': data}

        if exists is not None:
            self.data_list[exists['index']] = exists['data']
        else:
            self.data_list.append(data)

        json_string = object.object_to_json(data)

        with open(os.path.join(self.path, filename), 'w', encoding='utf-8') as f:
            rs = f.write(json_string)

        return rs


class LocalCsvDriver(Driver):
    df: pandas.DataFrame | None = None
    _TABLE_NAME = 'local'

    def __init__(self, config: dict):
        super().__init__(config)
        make_local_dir(config['path'])

        self.path = os.path.join(config['path'], 'local')
        self.df = self._all()

    def get_query(self):
        return dfquery.make(self._TABLE_NAME, self.df)

    def get(self, data: LocalSchema, data_id: str | int = None) -> LocalSchema | None:
        query = self.get_query()
        tbl = dfquery.table(self._TABLE_NAME)

        gen = tbl.name(data_id).select('*').where({
            'key': 'data_id',
            'operator': '==',
            'value': data_id
        })

        query.query(gen)

        result = query.build()

        first = None
        if self._TABLE_NAME in result:
            if data_id in result[self._TABLE_NAME]:
                if len(result[self._TABLE_NAME][data_id]) != 0:
                    first = result[self._TABLE_NAME][data_id][0]

        if first is None:
            return None

        data.map(first)
        return data

    def get_by_month(self, data: LocalSchema, year: int, month: int) -> list[LocalSchema]:
        year = str(year)
        month = str(month).zfill(2)

        query = self.get_query()
        query_name = f"{year}-{month}"
        gen = dfquery.table(self._TABLE_NAME).name(query_name)
        gen.select(['*']).where({
            "key": "data_id",
            "operator": "like",
            "value": f"{query_name}*"
        })

        query.query(gen)
        result = query.build()
        data_list = result[self._TABLE_NAME][query_name]

        return list(map(lambda x: copy.deepcopy(data).map(x), data_list))

    def _all(self) -> pandas.DataFrame:
        filename = 'local_all.csv'
        if self.df is not None:
            return self.df

        if os.path.exists(filename):
            return pandas.read_csv(os.path.join(self.path, filename))

        return pandas.DataFrame()

    def all(self, data: LocalSchema) -> list[LocalSchema]:
        df = self._all()
        df_dict = df.to_dict(orient='records')
        if isinstance(df_dict, list):
            data_list = []
            for d in df_dict:
                to_data = copy.deepcopy(data)
                to_data.map(d)
                data_list.append(to_data)
            return data_list
        return []

    @staticmethod
    def _to_df(data: LocalSchema | list[LocalSchema]):
        if isinstance(data, list):
            data_list = data
            data_list = list(map(lambda x: x.__dict__, data_list))
            df = pandas.DataFrame.from_records(data_list)
        else:
            df = pandas.DataFrame.from_records([data.__dict__])
        return df

    def save(self, data_id, data: LocalSchema) -> LocalSchema | None:
        data_list = self.all(LocalSchema())
        exists = None
        for i, exists_data in enumerate(data_list):
            if exists_data.data_id == data_id:
                exists = {'index': i, 'data': data}

        if exists is not None:
            data_list[exists['index']] = exists['data']
        else:
            data.data_id = data_id
            data_list.append(data)

        self.df = self._to_df(data_list)

        return data

    def commit(self):
        filename = 'local_all.csv'

        return self.df.to_csv(os.path.join(self.path, filename), index=False)

    def export_csv(self, path: str, data_list: list[LocalSchema]) -> str | None:
        df = self._to_df(data_list)
        return df.to_csv(path, index=False)

    def __del__(self):
        self.commit()
