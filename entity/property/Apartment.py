from entity.property.District import District
from entity.property.Property import Property
from entity.seller.Seller import Seller
from util.enums.UsageType import UsageType


class Apartment(Property):

    __repr_fields__ = ( 'have_elevator', 'have_parking', 'floor' ,)
    __str_fields__ = ( 'have_elevator', 'have_parking', 'floor' ,)


    def __init__(self, seller:Seller, area : float,
                 rooms : int, build_year : int,
                 district : District, address : str,
                 usage_type: UsageType,
                 have_elevator : bool, have_parking : bool,
                 floor : int):
        super().__init__(seller, area, rooms, build_year, district, address, usage_type)
        self.__have_elevator = have_elevator
        self.__have_parking = have_parking
        self.__floor = floor

    def show_all_of_details(self):
        return f"{super.__repr__(self)}, Have Elevator: {self.__have_elevator}, Have Parking: {self.__have_parking}, Floor: {self.__floor}"


    @property
    def have_elevator(self):
        return self.__have_elevator

    @property
    def have_parking(self):
        return self.__have_parking

    @property
    def floor(self):
        return self.__floor

    @have_elevator.setter
    def have_elevator(self, have_elevator):
        self.__have_elevator = have_elevator

    @have_parking.setter
    def have_parking(self, have_parking):
        self.__have_parking = have_parking

    @floor.setter
    def floor(self, floor):
        self.__floor = floor

    def __eq__(self, other):
        return super().__eq__(other) and self.__have_elevator == other.__have_elevator and self.__have_parking == other.__have_parking and self.__floor == other.__floor
    def __hash__(self):
        return super().__hash__()

