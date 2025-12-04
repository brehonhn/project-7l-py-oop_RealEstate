from entity.base.BaseEntity import BaseEntity
from entity.seller.Seller import Seller
from abc import ABC, abstractmethod

from entity.property.District import District
from util.enums.UsageType import UsageType


class Property(BaseEntity, ABC):

    __repr_fields__ = ('seller', 'area', 'rooms', 'build_year', 'district', 'address', 'usage_type' , )
    __str_fields__ = ('seller', 'area', 'rooms', 'build_year', 'district', 'address', 'usage_type' , )

    def __init__(self, seller: Seller, area: float,
                 rooms: int, build_year: int,
                 district : District, address : str,
                 usage_type : UsageType):
        super().__init__()
        self.__seller = seller
        self.__area = area
        self.__rooms = rooms
        self.__build_year = build_year
        self.__district = district
        self.__address = address
        self.__usage_type = usage_type

    @abstractmethod
    def show_all_of_details(self):
        pass

    @property
    def seller(self):
        return self.__seller

    @seller.setter
    def seller(self, seller):
        if isinstance(seller, Seller):
            self.__seller = seller

    @property
    def area(self):
        return self.__area

    @area.setter
    def area(self, area):
        if isinstance(area, float):
            self.__area = area

    @property
    def rooms(self):
        return self.__rooms

    @rooms.setter
    def rooms(self, rooms):
        if isinstance(rooms, int):
            self.__rooms = rooms

    @property
    def build_year(self):
        return self.__build_year

    @build_year.setter
    def build_year(self, build_year):
        if isinstance(build_year, int):
            self.__build_year = build_year

    @property
    def district(self):
        return self.__district

    @district.setter
    def district(self, district):
        if isinstance(district, District):
            self.__district = district

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, address):
        if isinstance(address, str):
            self.__address = address

    @property
    def usage_type(self):
        return self.__usage_type

    @usage_type.setter
    def usage_type(self, usage_type):
        if isinstance(usage_type, UsageType):
            self.__usage_type = usage_type


    def __eq__(self, other):
        if isinstance(other, Property):
            return (self.__seller == other.__seller and self.__area == other.__area and
                    self.__rooms == other.__rooms and self.__build_year == other.__build_year and
                    self.__district == other.__district and self.__address == other.__address)
        return False

    def __hash__(self):
        return hash((self.__seller, self.__area, self.__rooms, self.__build_year, self.__district, self.__address))
