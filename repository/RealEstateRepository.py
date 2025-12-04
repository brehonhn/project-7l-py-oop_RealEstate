# repository/real_estate_repository.py

from entity.base.BaseEntity import BaseEntity
from entity.seller.Seller import Seller
from entity.property.District import District
from entity.property.Apartment import Apartment
from entity.property.Villa import Villa      # یا Villa، هرچی اسم گذاشتی
from entity.property.Shop import Shop
from entity.listing.SaleListing import SaleListing
from entity.listing.RentListing import RentListing
from util.enums.UsageType import UsageType   # اگر این‌طوری تعریف کردی


class RealEstateRepository:
    """
    Repository in-memory:
    - داده نمونه می‌سازه (seed_data)
    - روی BaseEntity.objects_list کار می‌کند
    """

    @classmethod
    def seed_data(cls) -> None:
        """چند ملک + چند فایل نمونه بساز و تو objects_list ذخیره شود."""

        # ------ فروشنده‌ها ------
        seller1 = Seller(full_name="Ali Ahmadi", phone_number="09120000000")
        seller2 = Seller(full_name="Sara Hosseini", phone_number="09123334444")

        # ------ محله‌ها ------
        district1 = District("Vanak")
        district2 = District("Lavassan")
        district3 = District("Tehranpars")

        # ------ ملک‌ها (Propertyها) ------
        apt1 = Apartment(
            seller=seller1,
            area=110,
            rooms=3,
            build_year=2018,
            district=district1,
            address="Vanak St. No. 10",
            have_elevator=True,
            have_parking=True,
            floor=4,
            usage_type=UsageType.RESIDENTIAL,
        )

        villa1 = Villa(
            seller=seller2,
            area=320,
            rooms=4,
            build_year=2015,
            district=district2,
            address="Lavassan Blvd.",
            have_yard=True,
            floors=2,
            usage_type=UsageType.RESIDENTIAL,
        )

        shop1 = Shop(
            seller=seller1,
            area=60,
            rooms=1,
            build_year=2010,
            district=district3,
            address="Tehranpars Main St.",
            usage_type=UsageType.COMMERCIAL,
        )

        # ------ فایل‌ها (Listingها) ------
        # برای apt1 یک فایل فروش و یک فایل رهن/اجاره
        SaleListing(
            prop=apt1,
            price_per_meter=120_000_000,
            discount=5,
            swap=True,
        )

        RentListing(
            prop=apt1,
            deposit=800_000_000,
            rent=15_000_000,
            convertible=True,
            discount=3,
        )

        # برای ویلا فقط فروش
        SaleListing(
            prop=villa1,
            price_per_meter=90_000_000,
            discount=2,
            swap=False,
        )

        # برای مغازه فقط رهن/اجاره
        RentListing(
            prop=shop1,
            deposit=300_000_000,
            rent=12_000_000,
            convertible=False,
            discount=1,
        )

    # -----------------------------
    # متدهای کمکی برای خواندن داده
    # -----------------------------

    @classmethod
    def all_entities(cls):
        """همه‌ی objectهایی که تا الان ساخته شده‌اند."""
        return list(BaseEntity.objects_list)

    @classmethod
    def all_properties(cls):
        from entity.property.Property import Property
        return [obj for obj in BaseEntity.objects_list if isinstance(obj, Property)]

    @classmethod
    def all_listings(cls):
        from entity.listing.Listing import Listing
        return [obj for obj in BaseEntity.objects_list if isinstance(obj, Listing)]

    @classmethod
    def all_sale_listings(cls):
        from entity.listing.SaleListing import SaleListing
        return [obj for obj in BaseEntity.objects_list if isinstance(obj, SaleListing)]

    @classmethod
    def all_rent_listings(cls):
        from entity.listing.RentListing import RentListing
        return [obj for obj in BaseEntity.objects_list if isinstance(obj, RentListing)]

    @classmethod
    def search_sales(
        cls,
        district: str | None = None,
        min_price: float | None = None,   # قیمت کل
        max_price: float | None = None,
        min_area: float | None = None,
        max_area: float | None = None,
        min_rooms: int | None = None,
        max_rooms: int | None = None,
    ):
        """جستجوی فایل‌های فروش براساس محله، قیمت کل، متراژ و تعداد خواب."""
        from entity.listing.SaleListing import SaleListing
        results: list[SaleListing] = []

        for listing in cls.all_sale_listings():
            prop = listing.property  # ملک مربوط به این فایل

            # 1) محله
            if district is not None and prop.district.name != district:
                continue

            # 2) قیمت (اینجا قیمت کل را معیار می‌گیریم)
            total_price = listing.price_per_meter * prop.area
            if min_price is not None and total_price < min_price:
                continue
            if max_price is not None and total_price > max_price:
                continue

            # 3) متراژ
            if min_area is not None and prop.area < min_area:
                continue
            if max_area is not None and prop.area > max_area:
                continue

            # 4) تعداد خواب
            if min_rooms is not None and prop.rooms < min_rooms:
                continue
            if max_rooms is not None and prop.rooms > max_rooms:
                continue

            results.append(listing)

        return results

    # ------------ SEARCH FOR RENT LISTINGS ------------

    @classmethod
    def search_rents(
        cls,
        district: str | None = None,
        min_rent: float | None = None,   # اجاره ماهانه
        max_rent: float | None = None,
        min_area: float | None = None,
        max_area: float | None = None,
        min_rooms: int | None = None,
        max_rooms: int | None = None,
    ):
        """جستجوی فایل‌های رهن/اجاره براساس محله، اجاره، متراژ و تعداد خواب."""
        from entity.listing.RentListing import RentListing
        results: list[RentListing] = []

        for listing in cls.all_rent_listings():
            prop = listing.property  # ملک مربوط به این فایل

            # 1) محله
            if district is not None and prop.district.name != district:
                continue

            # 2) اجاره
            rent = listing.rent
            if min_rent is not None and rent < min_rent:
                continue
            if max_rent is not None and rent > max_rent:
                continue

            # 3) متراژ
            if min_area is not None and prop.area < min_area:
                continue
            if max_area is not None and prop.area > max_area:
                continue

            # 4) تعداد خواب
            if min_rooms is not None and prop.rooms < min_rooms:
                continue
            if max_rooms is not None and prop.rooms > max_rooms:
                continue

            results.append(listing)

        return results
