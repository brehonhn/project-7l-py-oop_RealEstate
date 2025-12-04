from entity.property.District import District
from entity.property.Property import Property
from entity.seller.Seller import Seller
from util.enums.UsageType import UsageType


class Villa(Property):

    __repr_fields__ = ( 'have_yard', 'floors' , )
    __str_fields__ = ( 'have_yard', 'floors' ,)

    def __init__(self,seller: Seller, area: float,
                 rooms: int, build_year: int,
                 district : District, address : str,
                 usage_type : UsageType, have_yard: bool,
        floors: int):
        super().__init__(seller, area, rooms, build_year, district, address, usage_type)
        self.__have_yard = have_yard
        self.__floors = floors

    @property
    def have_yard(self):
        return self.__have_yard

    @property
    def floors(self):
        return self.__floors

    @floors.setter
    def floors(self, floors):
        self.__floors = floors

    @have_yard.setter
    def have_yard(self, have_yard):
        self.__have_yard = have_yard

    def show_all_of_details(self):
        return f"{self.__repr__()}"

    def __eq__(self, other):
        return super().__eq__(other)

    def __hash__(self):
        return super().__hash__()