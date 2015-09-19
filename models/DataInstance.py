__author__ = 'fabrice'

class DataInstance:

    def __init__(self, line, class_index):
        self._row = line
        self._class_index = class_index

    def __getitem__(self, i):
        return self._row[i]

    def transform_attribute(self, function, attribute_index=None):
        index = attribute_index if attribute_index != None else self._class_index
        result = [
            (function(self._row[cell_index]) if cell_index==index else self._row[cell_index])
            for cell_index in range(len(self._row))
            ]
        return DataInstance(result, self._class_index)

    def create_row_without_attributes(self, index_set_to_remove):
        if self._class_index in index_set_to_remove:
            raise Exception("Cannot remove attribute which is the class (index : %s, indexes to remove : %s)" % (self._class_index, index_set_to_remove))
        new_row = []
        new_class_index_offset=0
        for i in range(len(self._row)):
            if i not in index_set_to_remove:
                new_row.append(self._row[i])
            else:
                if i < self._class_index:
                    new_class_index_offset+=1
        return new_row

    def __iter__(self):
           return iter(self._row)

    def __len__(self):
        return len(self._row)

    def __repr__(self):
        return repr(self._row)

    def get_class_value(self):
        return self._row[self._class_index]

    def to_csv_line(self, repr_config):
        return repr_config.delimiter.join([repr_config.get_repr_for_value(self[cell_index], cell_index) for cell_index in range(len(self))])