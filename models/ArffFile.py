__author__ = 'fabrice'

class ArffFile:
    _repr_config=None
    _dataset=None
    def __init__(self, name, dataset, data_repr_config=None):
        self._name = name
        self._headers = dataset.get_headers()
        self._repr_config = dataset.compute_csv_repr_config() if data_repr_config==None else data_repr_config
        self._dataset = dataset


    def to_arff(self):

        def repr_values(header_index):
            values = self._repr_config.get_values_for_header(header_index)
            return self._repr_config.delimiter.join([
                self._repr_config.get_repr_for_value(val, header_index) for val in values
            ])

        def data_type(header_index):
            if self._repr_config.is_numeric(header_index):
                return "numeric"
            return "{" + repr_values(header_index) + "}"


        attributes = "\n".join(
            [
                "@attribute %s %s" % (self._headers[i], data_type(i)) for i in range(len(self._headers))
            ]
        )

        csv_content = self._dataset.data_to_csv(self._repr_config)

        return """
@relation %s

%s

@data
%s
""" % (self._name, attributes, csv_content)