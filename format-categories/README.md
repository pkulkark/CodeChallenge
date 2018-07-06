# format-categories

The code to format the given nested category object to a flat list of objects is found in **format_json.py**.

The input is read from the url: https://res.cloudinary.com/esanjolabs/raw/upload/v1529967088/tests/categories-test.json

The output list of objects is written to a file **testout.txt** with each object containing the following attributes:
  * _objectID_: id of the category
  * _parent_id_: id of the closest parent category
  * _is_active_:
  * _position_:
  * _level_:
  * _product_count_: 
  * _name_: Name of the category
  * _name_ar_:
  * _tree_: Names of all parent categories and the current category joined using the character ' > ' . if no parent, leave current category name alone
  * _tree_ar_: Just like the tree attribute, but Arabic names
  * _ids_: List of ids of all parent categories and the current category id, in hierarchical order. If no parent, leave current category id alone
  * _path_:
  
The output file is created when the python file is executed.

## Running the file

The python file may be executed using the command:
```python
python3 format_json.py
```
