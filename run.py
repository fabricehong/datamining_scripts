from dataset_transform import generate_files

__author__ = 'fabrice'

jobsEventValue = 'http://liip.ch/en/jobs'

def prepareClass(value):
    if value== ('%s' % jobsEventValue):
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

def operations_split_in_two(dataname, dataset):
    new_dataset = dataset.transform_attribute(prepareClass)

    repr_config = new_dataset.compute_csv_repr_config()
    training_set, test_set = new_dataset.split_and_adjust_up(0.66)

    # generate data files
    training_set.name = dataname + "_trainingset"
    test_set.name = dataname + "_testset"

    # reassign repr config
    training_set.repr_config = repr_config
    test_set.repr_config = repr_config
    return [training_set, test_set]

def operations_split_in_one_reduce(dataname, dataset):
    training_set, test_set = operations_split_in_two_reduce(dataname, dataset)
    training_set.append(test_set)
    training_set.name = dataname + "_adjusted-down_splitted"
    return [training_set]

def operations_split_in_two_reduce(dataname, dataset):

    # egalize before class conversion
    dataset = dataset.adjust_down(jobsEventValue)
    dataset = dataset.transform_attribute(prepareClass)
    # egalize after class conversion
    dataset = dataset.adjust_down("job")
    repr_config = dataset.compute_csv_repr_config()
    dataset = dataset.randomize()
    training_set, test_set = dataset.split(0.66)


    # generate data files
    training_set.name = dataname + "_adjusted-down_trainingset"
    test_set.name = dataname + "_adjusted-down__testset"

    # reassign repr config
    training_set.repr_config = repr_config
    test_set.repr_config = repr_config
    return [training_set, test_set]

def operations_split_in_one(dataname, dataset):
    new_dataset = dataset.transform_attribute(prepareClass)

    result = new_dataset.split_training_and_test_in_one_dataset(0.66)

    # generate data files
    result.name = dataname + "_splitted"
    return [result]

def generate_split_with_attr(root_dir, dataname, class_index, attributes):
    def op(dataname, dataset):
        headers = dataset.get_headers()
        attr_to_remove = [attr for attr in headers if attr not in attributes]
        new_dataset = dataset.without_attributes(attr_to_remove)
        (training_set,) = operations_split_in_one_reduce(dataname, new_dataset)
        training_set.name = dataname + "_" + "_".join(
            [
                attr.split(":")[1][0] for attr in attributes
            ]
        )
        return [training_set]

    generate_files(root_dir, dataname, class_index, op, "arff")

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

#generate_files("/home/fabrice/datamining/GaRawDataReader/class_at_end/data", "class_at_end", 5, operations_split_in_two, "arff")

#generate_files("/home/fabrice/datamining/GaRawDataReader/class_at_end/data", "class_at_end", 5, operations_split_in_one, "csv")

generate_files("/home/fabrice/datamining/GaRawDataReader/dim_07_segments_vs_no_segments/data", "segments", 5, operations_split_in_two_reduce, "arff")
#generate_files("/home/fabrice/datamining/GaRawDataReader/class_at_end/data", "class_at_end", 5, operations_split_in_one_reduce, "arff")



#generate_split_with_attr("/home/fabrice/datamining/GaRawDataReader/dim_06_all_impossible/data", "all_impossible", 0,
#             ["ga:eventLabel", "ga:deviceCategory", "ga:country", "ga:medium", "ga:javaEnabled", "ga:userType"]
#             )

#for gen_attrs in get_all_attributes_combination(["ga:deviceCategory", "ga:country", "ga:medium", "ga:javaEnabled", "ga:userType"], 3):
#    attrs = ["ga:eventLabel"] + gen_attrs
#    generate_split_with_attr("/home/fabrice/datamining/GaRawDataReader/class_at_end/data", "segments", 5, attrs)
