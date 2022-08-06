#!/usr/bin/python3
"""Creates a FileStorage class."""
import json
import models
import os


class FileStorage:
    """
    serializes instances to a JSON file and
    deserializes JSON file to instances.
    """

    __file_path = "file.json"
    __objects = {}

    def __init__(self):
        """Initializes FileStorage."""
        super().__init__()

    def all(self):
        """Return the class attribute objects."""
        return FileStorage.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id."""
        if obj is not None:
            key = '{}.{}'.format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to JSON file (path: __file_path)"""
        file = FileStorage.__file_path

        with open(file, mode='w', encoding='utf-8') as f:
            f.write(json.dumps(FileStorage.__objects,
                    cls=models.base_model.BaseModelEncoder))

    def reload(self):
        """deserializes the JSON file to __objects"""
        file = FileStorage.__file_path
        if not os.path.exists(file):
            return
        try:
            with open(file, mode='r+', encoding='utf-8') as f:
                file_string = f.read()
                data = json.loads(file_string)
                for key, value in data.items():
                    model_name, model_id = key.split('.')
                    model = models.classes[model_name](**value)
                    self.new(model)
        except Exception as e:
            print(e)
