from entity.listing.Listing import Listing
from entity.property.Property import Property


class RentListing(Listing):
    __repr_fields__ = ("deposit", "rent", "convertible", "discount")
    __str_fields__  = ("deposit", "rent", "convertible", "discount")

    def __init__(self, prop: Property,
                 deposit: float,
                 rent: float,
                 convertible: bool = False,
                 discount: float = 0.0):
        super().__init__(prop)
        self.deposit = deposit
        self.rent = rent
        self.convertible = convertible
        self.discount = discount

    @property
    def rent(self):
        return self._rent

    @rent.setter
    def rent(self, value):
        self._rent = value

    @property
    def deposit(self):
        return self._deposit

    @deposit.setter
    def deposit(self, value):
        self._deposit = value

    @property
    def convertible(self):
        return self._convertible

    @convertible.setter
    def convertible(self, value):
        self._convertible = value

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        self._discount = value