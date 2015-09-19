from csv_transform import read_csv
from file_utils import write_to_file
from models.DataSet import DataSet

__author__ = 'fabrice'

def prepareClass(value):
    if value=='http://liip.ch/en/jobs':
        return 'job'
    else:
        return "nojob"

def prepareLanguage(val):
    value=str(val)
    if value.startswith("en"):
        return "en"
    if value.startswith("fr"):
        return "fr"
    if value.startswith("de"):
        return "de"
    if value.startswith("it"):
        return "it"
    if value.startswith("es"):
        return "es"
    if value.startswith("pt"):
        return "pt"
    return "other"

def split_and_balance(root_dir, data_name):
    def get_output_filename(name):
        return root_dir + "/" + name + ".arff"

    # prepare global dataset
    input_file = root_dir + "/" + data_name + ".csv"
    dataset = read_csv(input_file)
    dataset = dataset.transform_attribute(prepareClass)
    repr_config = dataset.compute_csv_repr_config()
    dataset = dataset.randomize()

    # prepare trainingset and testset
    training_set, test_set = dataset.split(0.66)

    training_set = training_set.balance_classes()
    test_set = test_set.balance_classes()

    training_set = training_set.randomize()
    test_set = test_set.randomize()

    # generate data files

    trainingset_name = data_name + "_trainingset"
    testset_name = data_name + "_testset"

    training_set_arff_content = training_set.to_arff(trainingset_name, repr_config)
    test_set_arff_content = test_set.to_arff(testset_name, repr_config)

    write_to_file(get_output_filename(trainingset_name), training_set_arff_content)
    write_to_file(get_output_filename(testset_name), test_set_arff_content)

    print(training_set_arff_content)
    print(test_set_arff_content)

split_and_balance("/home/fabrice/datamining/GaRawDataReader/dim_06_all_impossible/data", "all_impossible")
