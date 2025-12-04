from entity.base.BaseEntity import BaseEntity


class District(BaseEntity):

    __repr_fields__ = ("name",)
    __str_fields__ = ("name",)

    def __init__(self,name:str):
        super().__init__()
        self.__name = name


    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,name):
        self.__name = name


    def __eq__(self, other):
        return self.__name == other.name
    def __hash__(self):
        return hash(self.__name)

