from entity.property.District import District
from entity.property.Property import Property
from entity.seller.Seller import Seller
from util.enums.UsageType import UsageType


class Shop(Property):

    def __init__(self, seller: Seller, area: float, rooms: int, build_year: int, district: District, address: str,
                 usage_type: UsageType):
        super().__init__(seller, area, rooms, build_year, district, address, usage_type)

    def show_all_of_details(self):
        return f"{self.__repr__()}"
