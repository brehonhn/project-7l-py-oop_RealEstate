from entity.listing.Listing import Listing
from entity.property.Property import Property


class SaleListing(Listing):

    __repr_fields__ = ("price_per_meter", "discount", "swap")
    __str_fields__  = ("price_per_meter", "discount", "swap")
    def __init__(self, prop: Property,
                 price_per_meter: float,
                 discount: float = 0.0,
                 swap: bool = False):
        super().__init__(prop)
        self.price_per_meter = price_per_meter
        self.discount = discount
        self.swap = swap


    @property
    def price_per_meter(self):
        return self._price_per_meter

    @price_per_meter.setter
    def price_per_meter(self, value):
        self._price_per_meter = value

    @property
    def discount(self):
        return self._discount

    @discount.setter
    def discount(self, value):
        self._discount = value

    @property
    def swap(self):
        return self._swap

    @swap.setter
    def swap(self, value):
        self._swap = value

    def __eq__(self, other):
        return super().__eq__(other)
    
    def __hash__(self):
        return super().__hash__()