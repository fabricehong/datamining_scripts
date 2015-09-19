__author__ = 'fabrice'

class DataReprConfig:
    quote_char = "'"
    delimiter = ","



    def __init__(self, dataset):
        self._header_quoted=set()
        self._values_for_headers={}
        self._header_not_numeric=set()
        def is_numeric(str_val):
            try:
                float(str_val)
                return True
            except ValueError:
                return False

        for row in dataset.get_rows():
            for cell_index in range(len(row)):
                cell=row[cell_index]
                if cell_index in self._values_for_headers:
                    values = self._values_for_headers[cell_index]
                else:
                    values = set()
                values.add(cell)
                self._values_for_headers[cell_index] = values
                if ' ' in cell:
                    self._header_quoted.add(cell_index)
                if not is_numeric(cell):
                    self._header_not_numeric.add(cell_index)


    def is_quote_delimited(self, col_index):
        if col_index in self._header_quoted:
            return True
        return False

    def get_values_for_header(self, col_index):
        return self._values_for_headers[col_index]

    def is_numeric(self, col_index):
        return col_index not in self._header_not_numeric

    def get_repr_for_value(self, value, col_index):
        escaped_quote = '\\' + self.quote_char
        def escape_quote(val):
            return val.replace(self.quote_char, escaped_quote)

        if self.is_quote_delimited(col_index):
            return self.quote_char + escape_quote(value) + self.quote_char
        else:
            return value