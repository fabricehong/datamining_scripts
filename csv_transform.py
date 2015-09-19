from models.DataSet import DataSet

__author__ = 'fabrice'

import csv

delimiter = ','
quotechar = '"'


def read_csv(file):
    with open(file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        return DataSet([row for row in spamreader])

