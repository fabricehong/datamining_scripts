__author__ = 'fabrice'

from dataset_transform import *
from file_utils import *

dataset = read_csv("/home/me/input.csv")
dataset = dataset.transform_attribute(lambda val : "developer" if val=="https://www.liip.ch/en/jobs" else "not_developer")
dataset = dataset.randomize()
training_set, test_set = dataset.split(0.66)
write_to_file("/home/me/training_set.arff", training_set.to_arff())
write_to_file("/home/me/test_set.arff", test_set.to_arff())