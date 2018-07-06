import urllib.request
import json
import copy
import pprint


class FormattedObject(object):
    def __init__(self, obj_id, par_id, is_active, position, level,
                 product_count, name, name_ar, path):
        """
        Initialize the object with required fields
        """
        self.objectID = obj_id
        self.parent_id = par_id
        self.is_active = is_active
        self.position = position
        self.level = level
        self.product_count = product_count
        self.name = name
        self.name_ar = name_ar
        self.path = path
        self.tree = ""
        self.tree_ar = ""
        self.ids = None


def create_object(json_data):
    """
    Method to create object from the input json
    :param json_data: input json data
    :return:
    """
    obj_id = json_data.get('id')
    parent_id = json_data.get('parent_id')
    is_active = json_data.get('is_active')
    position = json_data.get('position')
    level = json_data.get('level')
    product_count = json_data.get('product_count')
    name = json_data.get('name')
    name_ar = json_data.get('name_ar')
    if not name_ar:
        name_ar = " "
    path = json_data.get('path')
    req_obj = FormattedObject(obj_id, parent_id, is_active, position, level, product_count, name,
                              name_ar, path)
    return req_obj


def create_child_object(data, id_list, tree_list, tree_ar_list):
    """
    Method to create object for children data
    :return:
    """
    child_obj = create_object(data)
    par_ids = copy.deepcopy(id_list)
    par_ids.append(child_obj.objectID)
    child_obj.ids = par_ids
    child_obj.tree = tree_list + ' > ' + child_obj.name
    child_obj.tree_ar = tree_ar_list + ' > ' + child_obj.name_ar
    objs.append(child_obj)
    if data.get('children_data'):
        for ch_data in data['children_data']:
            create_child_object(ch_data, child_obj.ids, child_obj.tree, child_obj.tree_ar)



url = 'https://res.cloudinary.com/esanjolabs/raw/upload/v1529967088/tests/categories-test.json'
input_json = urllib.request.urlopen(url).read()
py_json = json.loads(input_json.decode("utf-8"))
required_data = py_json['children_data'][0]['children_data']
objs = []
for each_category in required_data:
    obj = create_object(each_category)
    obj.ids = [obj.objectID]
    obj.tree = obj.name
    obj.tree_ar = obj.name_ar
    objs.append(obj)
    if each_category.get('children_data'):
        for child_data in each_category['children_data']:
            create_child_object(child_data, obj.ids, obj.tree, obj.tree_ar)

for each_obj in objs:
    with open('testout.txt', 'a', encoding="utf-8") as outfile:
        pprint.pprint(each_obj.__dict__, stream=outfile)

