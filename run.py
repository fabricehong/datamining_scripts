from dataset_transform import csv_to_arffs

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

dataname = "new_scripts"

def operations_split_in_two(dataset):
    new_dataset = dataset.transform_attribute(prepareClass)

    repr_config = new_dataset.compute_csv_repr_config()
    training_set, test_set = new_dataset.split_and_balance(0.66)

    # generate data files
    training_set.name = dataname + "_trainingset"
    test_set.name = dataname + "_testset"

    # reassign repr config
    training_set.repr_config = repr_config
    test_set.repr_config = repr_config
    return [training_set, test_set]

def operations_split_in_one(dataset):
    new_dataset = dataset.transform_attribute(prepareClass)

    result = new_dataset.split_training_and_test_in_one_dataset(0.66)

    # generate data files
    result.name = dataname + "_splitted"
    return [result]

def generate_training_and_test_set_for(root_dir, dataname, class_index, attributes):
    def op(dataset):
        headers = dataset.get_headers()
        attr_to_remove = [attr for attr in headers if attr not in attributes]
        new_dataset = dataset.without_attributes(attr_to_remove)
        (training_set,) = operations_split_in_one(new_dataset)
        training_set.name = dataname + "_" + "_".join(
            [
                attr.split(":")[1][0] for attr in attributes
            ]
        )
        return [training_set]

    csv_to_arffs(root_dir, dataname, class_index, op)

def generate_all_sub_combination(the_list, min):
    if len(the_list)<min:
        return
    yield the_list
    for elem in the_list:
        l = list(the_list)
        l.remove(elem)
        for x in generate_all_sub_combination(l, min):
            yield x

def get_all_attributes_combination(the_list, min):
    result = []
    for lst in generate_all_sub_combination(the_list, min):
        if lst not in result:
            result.append(lst)
    return sorted(result, key=lambda x:len(x), reverse=True)

csv_to_arffs("/home/fabrice/datamining/GaRawDataReader/new_scripts/data", dataname, 5, operations_split_in_two)

#generate_training_and_test_set_for("/home/fabrice/datamining/GaRawDataReader/new_scripts/data", dataname,
#             ["ga:eventLabel", "ga:deviceCategory", "ga:country", "ga:medium", "ga:javaEnabled", "ga:userType"]
#             )

#for gen_attrs in get_all_attributes_combination(["ga:deviceCategory", "ga:country", "ga:medium", "ga:javaEnabled", "ga:userType"], 3):
#    attrs = ["ga:eventLabel"] + gen_attrs
#    generate_training_and_test_set_for("/home/fabrice/datamining/GaRawDataReader/new_scripts/data", dataname, 5, attrs)
