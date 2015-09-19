from collections import Counter
import operator
from models.ArffFile import ArffFile
from models.DataReprConfig import DataReprConfig
from models.DataInstance import DataInstance

__author__ = 'fabrice'

import random

delimiter = ','
quotechar = "'"

class DataSet:
    _rows = []
    _class_index=None
    _headers=[]

    def __init__(self, rows, class_index=0, headers=None):
        if headers==None:
            self._headers=DataInstance(rows[0], class_index)
            r=rows[1:]
        else:
            self._headers=headers
            r=rows
        self._rows = [DataInstance(row, class_index) for row in r]
        self._class_index = class_index

    def randomize(self):
        new_rows = list(self._rows)
        random.shuffle(new_rows)
        return self.create_data_set(new_rows)

    def transform_attribute(self, function, attribute_index=None):
        return self.create_data_set([row.transform_attribute(function, attribute_index) for row in self._rows])

    def get_rows_with_class(self, className):
        my_list = [row for row in self._rows if row.get_class_value() == className]
        return self.create_data_set(my_list)

    def get_rows(self):
        return self._rows

    def to_csv(self, repr_config=None):
        if repr_config == None:
            rc = self.compute_csv_repr_config()
        else:
            rc = repr_config
        return self._headers.to_csv_line(rc) + "\n" + self.data_to_csv(rc)

    def data_to_csv(self, repr_config=None):
        if repr_config == None:
            rc = self.compute_csv_repr_config()
        else:
            rc = repr_config
        return '\n'.join([row.to_csv_line(rc) for row in self._rows])

    def compute_csv_repr_config(self):
        return DataReprConfig(self)

    def balance_classes(self):
        new_dataset = self.create_data_set(list(self._rows))
        counter = Counter([row.get_class_value() for row in new_dataset])
        sorted_class_count = sorted(counter.items(), key=operator.itemgetter(1))
        max = sorted_class_count[-1][1]
        for item in sorted_class_count:
            instances_to_clone = max - item[1]
            new_dataset.clone_random_class_instances(item[0], instances_to_clone)
        return new_dataset

    def clone_random_class_instances(self, class_name, instances_to_clone):
        instances_with_class_name=self.get_rows_with_class(class_name)
        for i in range(instances_to_clone):
            row_to_clone = instances_with_class_name[random.randint(0, len(instances_with_class_name)-1)]
            self._rows.append(row_to_clone)

    def create_data_set(self, rows):
        return DataSet(rows, self._class_index, self._headers)

    def get_headers(self):
        return self._headers

    def __len__(self):
        return len(self._rows)

    def __getitem__(self, item):
        return self._rows[item]

    def split(self, percent):
        split_index = int(len(self._rows)*percent)
        return [
            self.create_data_set(self._rows[:split_index]),
            self.create_data_set(self._rows[split_index:])
        ]

    def to_arff(self, name, data_repr_config=None):
        self.compute_csv_repr_config() if data_repr_config==None else data_repr_config
        return ArffFile(name, self, data_repr_config).to_arff()

