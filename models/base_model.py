#!/usr/bin/python3
"""base class for all models"""

from uuid import uuid4
from datetime import datetime
import models
from json import JSONEncoder


class BaseModel:
    """
    Base class for other classes to inherit from
    """

    def __init__(self, *args, **kwargs):
        """Initialize the instance of the BaseModel"""
        if kwargs:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                elif key == "__class__":
                    continue

                setattr(self, key, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """Return a string representation of the BaseModel class"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Update the public instance attribute updated_at to current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the BaseModel class"""
        dict_repr = {}
        for key, value in self.__dict__.items():
            dict_repr[key] = value
            if isinstance(value, datetime):
                dict_repr[key] = value.strftime('%Y-%m-%dT%H:%M:%S.%f')
        dict_repr["__class__"] = type(self).__name__
        return dict_repr


class BaseModelEncoder(JSONEncoder):
    """JSON Encoder for BaseModel class"""

    def default(self, o):
        """default method for JSONEncoder"""
        if isinstance(o, BaseModel):
            return o.to_dict()
        return super().default(o)
