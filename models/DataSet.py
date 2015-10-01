from collections import Counter
import operator
import itertools
from models.ArffFile import ArffFile
from models.DataReprConfig import DataReprConfig
from models.DataInstance import DataInstance

__author__ = 'fabrice'

import random

delimiter = ','
quotechar = "'"

class DataSet:
    def __init__(self, rows, class_index=None, headers=None):
        if len(rows)==0:
            raise Exception("no rows provided")
        class_column_id = len(rows[0])-1 if class_index==None else class_index
        self.repr_config=None
        self.name="no_name"
        if headers==None:
            self._headers=DataInstance(rows[0], class_column_id)
            r=rows[1:]
        else:
            self._headers=headers
            r=rows
        self._rows = [DataInstance(row, class_column_id) for row in r]
        self._class_index = class_column_id

    def randomize(self):
        new_rows = list(self._rows)
        random.shuffle(new_rows)
        return self.create_data_set(new_rows)

    def transform_attribute(self, function, attribute_index=None):
        return self.create_data_set([row.transform_attribute(function, attribute_index) for row in self._rows])

    def get_rows_with_class(self, className):
        my_list = [row for row in self._rows if row.get_class_value() == className]
        return self.create_data_set(my_list)

    def get_rows_indexes_with_class(self, className):
        my_list = [i for i in range(len(self._rows)) if self._rows[i].get_class_value() == className]
        return my_list

    def get_rows(self):
        return self._rows

    def to_csv(self):
        rc = self.get_repr_config()
        return self._headers.to_csv_line(rc) + "\n" + self.data_to_csv(rc)

    def data_to_csv(self, repr_config=None):
        rc = self.get_repr_config() if repr_config==None else repr_config
        return '\n'.join([row.to_csv_line(rc) for row in self._rows])

    def get_repr_config(self):
        if self.repr_config == None:
            rc = self.compute_csv_repr_config()
        else:
            rc = self.repr_config
        return rc

    def compute_csv_repr_config(self):
        return DataReprConfig(self)

    def adjust_up(self):
        new_dataset = self.create_data_set(list(self._rows))
        counter = Counter([row.get_class_value() for row in new_dataset])
        sorted_class_count = sorted(counter.items(), key=operator.itemgetter(1))
        max = sorted_class_count[-1][1]
        for item in sorted_class_count:
            instances_to_clone = max - item[1]
            new_dataset.clone_random_class_instances(item[0], instances_to_clone)
        return new_dataset

    def adjust_down(self, referenceClass):
        new_dataset = self.create_data_set(list(self._rows))
        counter = Counter([row.get_class_value() for row in new_dataset])
        sorted_class_count = sorted(counter.items(), key=operator.itemgetter(1))
        if referenceClass not in counter:
            raise Exception("Reference '%s' not in found class values : %s" % (referenceClass, sorted_class_count.keys()))

        max = counter[referenceClass]
        for item in sorted_class_count:
            instances_to_remove = item[1] - max
            if (instances_to_remove>0):
                new_dataset.remove_random_class_instances(item[0], instances_to_remove)
        return new_dataset

    def clone_random_class_instances(self, class_name, instances_to_clone):
        instances_with_class_name=self.get_rows_with_class(class_name)
        for i in range(instances_to_clone):
            row_to_clone = instances_with_class_name[random.randint(0, len(instances_with_class_name)-1)]
            self._rows.append(row_to_clone)

    def remove_random_class_instances(self, class_name, instances_to_remove):
        indexes_for_classname=self.get_rows_indexes_with_class(class_name)
        indexes_to_keep = random.sample(indexes_for_classname, instances_to_remove)
        self._rows = [self._rows[i] for i in range(len(self._rows)) if i not in indexes_to_keep]

    def create_data_set(self, rows, new_name="new"):
        data_set = DataSet(rows, self._class_index, self._headers)
        data_set.repr_config = self.repr_config
        data_set.name = self.name + "-" + new_name
        return data_set

    def get_headers(self):
        return self._headers

    def __len__(self):
        return len(self._rows)

    def __getitem__(self, item):
        return self._rows[item]

    def split(self, percent):
        split_index = int(len(self._rows)*percent)
        return [
            self.create_data_set(self._rows[:split_index], "training"),
            self.create_data_set(self._rows[split_index:], "test")
        ]

    def to_arff(self):
        return ArffFile(self.name, self).to_arff()

    def split_and_adjust_up(self, percent_split):
        new_set = self.randomize()

        # prepare trainingset and testset
        training_set, test_set = new_set.split(percent_split)

        training_set = training_set.adjust_up()
        test_set = test_set.adjust_up()

        training_set = training_set.randomize()
        test_set = test_set.randomize()

        return (training_set, test_set)

    def split_training_and_test_in_one_dataset(self, percent):
        training_set, test_set = self.split_and_adjust_up(percent)
        training_set.append(test_set)
        return training_set

    def append(self, dataset):
        if self._headers is not dataset._headers:
            raise Exception("Impossible to append dataset that have not the same headers")
        self._rows.extend(dataset._rows)

    def without_attributes(self, attributes):
        def quantify(lst, fct):
            x = 0
            for elem in lst:
                if fct(elem):
                    x+=1
            return x
        if not set(self._headers).issuperset(set(attributes)):
            raise Exception("attributes '%s' are not in '%s'" % (attributes, self._headers))

        unwanted_indexes = set(
            [
                self._headers._row.index(attr) for attr in attributes
            ]
        )

        new_class_index = self._class_index - quantify(unwanted_indexes, lambda index : index < self._class_index)

        new_headers = DataInstance(self._headers.create_row_without_attributes(unwanted_indexes), new_class_index)

        new_rows = [
            row.create_row_without_attributes(unwanted_indexes) for row in self._rows
        ]
        return DataSet(new_rows, new_class_index, new_headers)
