from enum import Enum


class PropertyType(Enum):
    APARTMENT = {"id": 1, "name": "apartment"}
    VILLA = {"id": 2, "name": "villa"}
    SHOP = {"id": 3, "name": "shop"}


    @staticmethod
    def get_name(id):
        for property_type in PropertyType:
            if property_type.value["id"] == id:
                return property_type.value["name"]
        return None


    @staticmethod
    def get_id(name):
        for property_type in PropertyType:
            if property_type.value["name"] == name:
                return property_type.value["id"]
        return None