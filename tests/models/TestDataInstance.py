from models.DataInstance import DataInstance

__author__ = 'fabrice'

import unittest

class TestDataInstance(unittest.TestCase):

    def test_without_attributes(self):
        datainstance = DataInstance([1, 2, 3], 1)
        new_datainstance = datainstance.without_attributes(set([0, 2]))
        self.assertEqual(new_datainstance._class_index, 0)
        self.assertEqual(new_datainstance._row, [2])

if __name__ == '__main__':
    unittest.main()