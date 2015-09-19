import unittest
from models.DataInstance import DataInstance
from models.DataSet import DataSet

__author__ = 'fabrice'

class TestDataSet(unittest.TestCase):

    def test_without_attributes(self):
        class_index = 1
        dataset = DataSet([["1","2","3"]], class_index, DataInstance(["un", "deux", "trois"], class_index))
        new_dataset = dataset.without_attributes(["un", "trois"])
        self.assertEqual(new_dataset._headers._row, ["deux"])
        self.assertEqual(new_dataset.get_repr_config().get_values_for_header(0), set(["2"]))

if __name__ == '__main__':
    unittest.main()