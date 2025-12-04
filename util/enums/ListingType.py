from enum import Enum


class ListingType(Enum):
    Sale = {"id": 1, "name": "Sale"}
    Rent = {"id": 2, "name": "Rent/Deposit"}

    @staticmethod
    def get_listing_type_by_id(id):
        for listing_type in ListingType:
            if listing_type.value["id"] == id:
                return listing_type
        return None

    @staticmethod
    def get_listing_type_by_name(name):
        for listing_type in ListingType:
            if listing_type.value["name"] == name:
                return listing_type
        return None