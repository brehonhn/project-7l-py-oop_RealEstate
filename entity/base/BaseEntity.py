from abc import ABC

from util.metaclass.AutoReprStrMeta import AutoReprStrMeta


class BaseEntity(ABC,metaclass=AutoReprStrMeta):
    __repr_fields__ = ("id",)
    __str_fields__ = ("id",)

    _id = 0
    objects_list = None

    def __init__(self):
        self._id = self.generate_id()
        self.store(self)

    @classmethod
    def generate_id(cls):
        cls._id += 1
        return cls._id

    @classmethod
    def store(cls, obj):
        if cls.objects_list is None:
            cls.objects_list = list()
        cls.objects_list.append(obj)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    def __eq__(self, other):
        return self._id == other.__id

    def __hash__(self):
        return hash(self._id)
