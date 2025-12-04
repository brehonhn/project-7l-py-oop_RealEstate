from entity.base.BaseEntity import BaseEntity


class Seller(BaseEntity):
    __repr_fields__ = ("full_name", "phone_number",)
    __str_fields__ = ("full_name", "phone_number",)


    def __init__(self, full_name: str, phone_number : str):
        super().__init__()
        self.__full_name = full_name
        self.__phone_number = phone_number

    @property
    def full_name(self):
        return self.__full_name

    @full_name.setter
    def full_name(self, value):
        self.__full_name = value

    @property
    def phone_number(self):
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = value


    def __eq__(self, other):
        return super().__eq__(other) and self.full_name == other.full_name and self.phone_number == other.phone_number

    def __hash__(self):
        return super().__hash__()



