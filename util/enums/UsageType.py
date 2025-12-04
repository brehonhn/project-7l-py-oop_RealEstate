from enum import Enum


class UsageType(Enum):
    COMMERCIAL = {"id": 1, "name": "commercial"}
    OFFICE = {"id": 2, "name": "office"}
    RESIDENTIAL = {"id": 3, "name": "residential"}

    @staticmethod
    def get_usage_type_by_id(id):
        for usage_type in UsageType:
            if usage_type.value["id"] == id:
                return usage_type
        return None

    @staticmethod
    def get_usage_type_by_name(name):
        for usage_type in UsageType:
            if usage_type.value["name"] == name:
                return usage_type
        return None
