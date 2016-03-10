Split training and test set:
```python
from dataset_transform import *
from file_utils import *

dataset = read_csv("/home/me/input.csv")
dataset = dataset.transform_attribute(lambda val : "developer" if val=="https://www.liip.ch/en/jobs" else "not_developer")
dataset = dataset.randomize()
training_set, test_set = dataset.split(0.66)
write_to_file("/home/me/training_set.arff", training_set.to_arff())
write_to_file("/home/me/test_set.arff", test_set.to_arff())
```

Transform attribute:
```python
dataset = read_csv("/home/me/input.csv")
dataset.transform_attribute(lambda x : "mobile_OS" if x in ['Windows Phone', 'Android', 'iOS'] else x, 1)
write_to_file("/home/me/output.csv", dataset.to_csv())
```
Equivalent to:
```python
dataset = read_csv("/home/me/input.csv")
dataset.merge_values(['Windows Phone', 'Android', 'iOS'], "mobile_OS", 1)
write_to_file("/home/me/output.csv", dataset.to_csv())
```
