from file_utils import write_to_file
from models.DataSet import DataSet

__author__ = 'fabrice'

import csv

delimiter = ','
quotechar = '"'

def read_csv(file, class_index):
    with open(file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        return DataSet([row for row in spamreader], class_index)





def generate_files(root_dir, data_name, class_index, operations, extension):
    def get_output_filename(name):
        return root_dir + "/" + name + "." + extension

    # prepare global dataset
    input_file = root_dir + "/" + data_name + ".csv"
    dataset = read_csv(input_file, class_index)
    list_of_datasets = operations(data_name, dataset)

    for ds in list_of_datasets:
        if extension=="csv":
            content = ds.to_csv()
        elif extension=="arff":
            content = ds.to_arff()
        else:
            raise Exception("unmanaged extension : " + extension)
        write_to_file(get_output_filename(ds.name), content)
        print(content)