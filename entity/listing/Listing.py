from abc import ABC
from entity.base.BaseEntity import BaseEntity
from entity.property.Property import Property


class Listing(BaseEntity,ABC):

    __repr_fields__ = ('property' ,)
    __str_fields__ = ('property' ,)


    def __init__(self, prop: Property):
        super().__init__()
        self.__property = prop

    @property
    def property(self)-> Property:
        return self.__property

    @property.setter
    def property(self, prop: Property):
        self.__property = prop

    def __eq__(self, other):
        return self.__property == other.property

    def __hash__(self):
        return hash(self.__property)