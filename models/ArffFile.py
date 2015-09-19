__author__ = 'fabrice'

class ArffFile:
    def __init__(self, name, dataset):
        self._name = name
        self._headers = dataset.get_headers()
        self._dataset = dataset


    def to_arff(self):
        rc = self._dataset.get_repr_config()
        def repr_values(header_index):
            values = rc.get_values_for_header(header_index)
            return rc.delimiter.join([
                rc.get_repr_for_value(val, header_index) for val in values
            ])

        def data_type(header_index):
            if rc.is_numeric(header_index):
                return "numeric"
            return "{" + repr_values(header_index) + "}"


        attributes = "\n".join(
            [
                "@attribute %s %s" % (self._headers[i], data_type(i)) for i in range(len(self._headers))
            ]
        )

        csv_content = self._dataset.data_to_csv()

        return """
@relation %s

%s

@data
%s
""" % (self._name, attributes, csv_content)