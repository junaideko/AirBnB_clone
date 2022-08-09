#!/usr/bin/python3
"""
File storage:  serializes instances to a JSON file and
    deserializes JSON file to instances:
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State


# class Objects(dict):
#     """class object"""

#     def __getitem__(self, key):
#         """get item"""
#         try:
#             return super(Objects, self).__getitem__(key)
#         except Exception as e:
#             raise Exception("** no instance found **")

#     def pop(self, key):
#         """pop item"""
#         try:
#             return super(Objects, self).pop(key)
#         except Exception as e:
#             raise Exception("** no instance found **")

class FileStorage:
    """
    serializes instances to a JSON file and
    deserializes JSON file to instances.
    """

    __file_path = "file.json"
    __objects = {}

    # def __init__(self):
    #     """init method"""
    #     super().__init__()

    def all(self):
        """return the class atribute objects"""
        return type(self).__objects

    def reset(self):
        """clear data on __object (cache)"""
        self.__objects.clear()

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        objNameId = obj.__class__.__name__ + "." + obj.id
        type(self).__objects[objNameId] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path)"""

        with open(type(self).__file_path, "w", encoding='utf-8') as file:
            dict_storage = {}
            for key, val in type(self).__objects.items():
                dict_storage[key] = val.to_dict()
            json.dump(dict_storage, file)

    def reload(self):
        """deserializes the JSON file to __objects"""

        try:
            with open(type(self).__file_path, encoding='utf-8') as file:
                objdict = json.load(file)
                for obj in objdict.values():
                    cls_name = obj["__class__"]
                    del obj["__class__"]
                    self.new(eval(cls_name)(**obj))
        except FileNotFoundError:
            return

    def update(self, obj_name, obj_id, attr, value):
        """update object with id `obj_id`"""
        model = self.__objects["{}.{}".format(obj_name, obj_id)]
        setattr(model, attr, value)

    def find(self, obj_name, obj_id):
        """find object with id `obj_id`"""
        return self.__objects["{}.{}".format(obj_name, obj_id)]

    def delete(self, obj_name, obj_id):
        """
        delete object with id `obj_id`
        """
        return self.__objects.pop("{}.{}".format(obj_name, obj_id))
