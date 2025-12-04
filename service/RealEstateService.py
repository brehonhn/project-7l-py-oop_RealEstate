# service/real_estate_service.py

from typing import Optional

from repository.RealEstateRepository import RealEstateRepository

# این importها را با ساختار واقعی پروژه‌ات هماهنگ کن
from entity.seller.Seller import Seller
from entity.property.District import District
from entity.property.Apartment import Apartment
from entity.property.Villa import Villa      # یا Villa اگر این‌طوری نوشتی
from entity.property.Shop import Shop
from entity.listing.SaleListing import SaleListing
from entity.listing.RentListing import RentListing
from entity.base.BaseEntity import BaseEntity
from util.enums.UsageType import UsageType


# کدهای ANSI برای رنگ (اگر نخواستیش می‌تونی خالی‌شون کنی)
class Colors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class RealEstateService:
    def __init__(self) -> None:
        RealEstateRepository.seed_data()

    # ------------ helper برای ساخت label ملک، بدون نیاز به title ------------

    def _prop_label(self, p) -> str:
        """اگر title وجود داشت از آن استفاده می‌کنیم، در غیر این صورت
        یک متن جایگزین براساس نوع کلاس و محله می‌سازیم."""
        title = getattr(p, "title", None)
        district_name = getattr(getattr(p, "district", None), "name", "")
        cls_name = type(p).__name__
        if title:
            if district_name:
                return f"{title} ({cls_name} در {district_name})"
            return f"{title} ({cls_name})"
        else:
            if district_name:
                return f"{cls_name} در {district_name}"
            return cls_name

    # =================== حلقه اصلی منو ===================

    def run(self) -> None:
        while True:
            self.show_main_menu()
            choice = input(Colors.OKCYAN + "👉 انتخاب شما: " + Colors.ENDC).strip()

            if choice == "1":
                self.menu_create_property()
            elif choice == "2":
                self.menu_create_listing()
            elif choice == "3":
                self.menu_list_properties()
            elif choice == "4":
                self.menu_list_listings()
            elif choice == "5":
                self.menu_search_sales()
            elif choice == "6":
                self.menu_search_rents()
            elif choice == "7":
                self.menu_delete_property()
            elif choice == "8":
                self.menu_delete_listing()
            elif choice == "9":
                self.menu_update_property()
            elif choice == "0":
                print(Colors.WARNING + "خروج از سیستم مشاور املاک..." + Colors.ENDC)
                break
            else:
                print(Colors.FAIL + "❌ گزینه نامعتبر. دوباره تلاش کنید." + Colors.ENDC)

    def show_main_menu(self) -> None:
        print("\n" + "═" * 50)
        print(f"{Colors.BOLD}{Colors.OKBLUE}   🏠  سیستم مدیریت مشاور املاک  🏠{Colors.ENDC}")
        print("═" * 50)
        print(" 1) ➕ ثبت ملک جدید")
        print(" 2) 📝 ثبت فایل (فروش / رهن-اجاره) برای یک ملک")
        print(" 3) 📋 مشاهده لیست ملک‌ها")
        print(" 4) 📂 مشاهده لیست فایل‌ها")
        print(" 5) 🔍 جستجو در فایل‌های فروش")
        print(" 6) 🔎 جستجو در فایل‌های رهن/اجاره")
        print(" 7) ❌ حذف ملک (به‌همراه فایل‌های مرتبط)")
        print(" 8) 🗑 حذف فایل (Listing)")
        print(" 9) ✏️ ویرایش اطلاعات ملک")
        print(" 0) 🚪 خروج")
        print("─" * 50)

    # =================== ابزارهای کمکی ===================

    def _input_int(self, prompt: str, allow_empty: bool = False) -> Optional[int]:
        while True:
            s = input(prompt).strip()
            if allow_empty and s == "":
                return None
            try:
                return int(s)
            except ValueError:
                print(Colors.FAIL + "❌ عدد صحیح وارد کنید." + Colors.ENDC)

    def _input_float(self, prompt: str, allow_empty: bool = False) -> Optional[float]:
        while True:
            s = input(prompt).strip()
            if allow_empty and s == "":
                return None
            try:
                return float(s)
            except ValueError:
                print(Colors.FAIL + "❌ عدد (int/float) وارد کنید." + Colors.ENDC)

    def _select_usage_type(self) -> UsageType:
        print(Colors.OKBLUE + "نوع کاربری ملک را انتخاب کنید:" + Colors.ENDC)
        print(" 1) مسکونی")
        print(" 2) تجاری")
        print(" 3) اداری")
        while True:
            choice = input("👉 انتخاب: ").strip()
            if choice == "1":
                return UsageType.RESIDENTIAL
            if choice == "2":
                return UsageType.COMMERCIAL
            if choice == "3":
                return UsageType.OFFICE
            print(Colors.FAIL + "❌ گزینه نامعتبر." + Colors.ENDC)

    def _get_property_by_id(self, prop_id: int):
        for p in RealEstateRepository.all_properties():
            if getattr(p, "id", None) == prop_id:
                return p
        return None

    def _get_listing_by_id(self, listing_id: int):
        for l in RealEstateRepository.all_listings():
            if getattr(l, "id", None) == listing_id:
                return l
        return None

    # =================== 1) ثبت ملک جدید ===================

    def menu_create_property(self) -> None:
        print("\n" + "-" * 40)
        print(Colors.BOLD + "➕ ثبت ملک جدید" + Colors.ENDC)
        print("-" * 40)
        print("نوع ملک:")
        print(" 1) آپارتمان")
        print(" 2) ویلا/خانه")
        print(" 3) مغازه")

        kind = None
        while kind not in ("1", "2", "3"):
            kind = input("👉 انتخاب نوع ملک: ").strip()

        full_name = input("نام و نام خانوادگی مالک/فروشنده: ").strip()
        phone = input("شماره تماس: ").strip()
        seller = Seller(full_name=full_name, phone_number=phone)

        district_name = input("نام محله: ").strip()
        district = District(district_name)

        address = input("آدرس: ").strip()
        area = self._input_float("متراژ (متر): ")
        rooms = self._input_int("تعداد خواب: ")
        build_year = self._input_int("سال ساخت: ")
        usage_type = self._select_usage_type()

        # اگر مدل‌ات title ندارد، این خط را می‌توانی برداری
        # یا یک عنوان ساده با address بسازی
        title = input("عنوان (مثلاً «آپارتمان نوساز» - می‌تونی خالی بگذاری): ").strip()
        if not hasattr(seller, "title") and not title:
            # فقط یک متن ساده برای سازگاری، اگر در مدل اصلی title نداشتی
            title = None

        if kind == "1":
            have_elevator = input("آسانسور دارد؟ (y/n): ").strip().lower() == "y"
            have_parking = input("پارکینگ دارد؟ (y/n): ").strip().lower() == "y"
            floor = self._input_int("طبقه: ")
            apt = Apartment(
                seller=seller,
                area=area,
                rooms=rooms,
                build_year=build_year,
                district=district,
                address=address,
                have_elevator=have_elevator,
                have_parking=have_parking,
                floor=floor,
                usage_type=usage_type,
                title=title if "title" in Apartment.__dict__ else None,
            )
            print(Colors.OKGREEN + f"✅ آپارتمان با id={apt.id} ثبت شد." + Colors.ENDC)

        elif kind == "2":
            yard = input("حیاط دارد؟ (y/n): ").strip().lower() == "y"
            floors = self._input_int("تعداد طبقات: ")
            villa = Villa(
                seller=seller,
                area=area,
                rooms=rooms,
                build_year=build_year,
                district=district,
                address=address,
                have_yard=yard,
                floors=floors,
                usage_type=usage_type,
                title=title if "title" in Villa.__dict__ else None,
            )
            print(Colors.OKGREEN + f"✅ ویلا با id={villa.id} ثبت شد." + Colors.ENDC)

        else:
            shop = Shop(
                seller=seller,
                area=area,
                rooms=rooms,
                build_year=build_year,
                district=district,
                address=address,
                usage_type=usage_type,
                title=title if "title" in Shop.__dict__ else None,
            )
            print(Colors.OKGREEN + f"✅ مغازه با id={shop.id} ثبت شد." + Colors.ENDC)

    # =================== 2) ثبت فایل برای ملک ===================

    def menu_create_listing(self) -> None:
        print("\n" + "-" * 40)
        print(Colors.BOLD + "📝 ثبت فایل (آگهی) جدید" + Colors.ENDC)
        print("-" * 40)
        self.menu_list_properties(show_header=False)
        prop_id = self._input_int("id ملک موردنظر را وارد کنید: ")
        prop = self._get_property_by_id(prop_id)
        if prop is None:
            print(Colors.FAIL + "❌ ملکی با این id پیدا نشد." + Colors.ENDC)
            return

        print("نوع فایل:")
        print(" 1) فروش")
        print(" 2) رهن/اجاره")
        kind = None
        while kind not in ("1", "2"):
            kind = input("👉 انتخاب: ").strip()

        if kind == "1":
            price_per_meter = self._input_float("قیمت هر متر: ")
            discount = self._input_float("درصد تخفیف (مثلاً 5): ", allow_empty=True) or 0.0
            swap = input("معاوضه دارد؟ (y/n): ").strip().lower() == "y"
            listing = SaleListing(
                prop=prop,
                price_per_meter=price_per_meter,
                discount=discount,
                swap=swap,
            )
            print(Colors.OKGREEN + f"✅ فایل فروش با id={listing.id} ثبت شد." + Colors.ENDC)
        else:
            deposit = self._input_float("مبلغ رهن: ")
            rent = self._input_float("مبلغ اجاره: ")
            convertible = input("قابل تبدیل است؟ (y/n): ").strip().lower() == "y"
            discount = self._input_float("درصد تخفیف (مثلاً 5): ", allow_empty=True) or 0.0
            listing = RentListing(
                prop=prop,
                deposit=deposit,
                rent=rent,
                convertible=convertible,
                discount=discount,
            )
            print(Colors.OKGREEN + f"✅ فایل رهن/اجاره با id={listing.id} ثبت شد." + Colors.ENDC)

    # =================== 3) لیست ملک‌ها ===================

    def menu_list_properties(self, show_header: bool = True) -> None:
        if show_header:
            print("\n" + "-" * 40)
            print(Colors.BOLD + "📋 لیست همه ملک‌ها" + Colors.ENDC)
            print("-" * 40)

        props = RealEstateRepository.all_properties()
        if not props:
            print("هیچ ملکی ثبت نشده است.")
            return

        for p in props:
            label = self._prop_label(p)
            district_name = getattr(getattr(p, "district", None), "name", "")
            print(
                f"• id={p.id} | {label} | "
                f"{getattr(p, 'area', '?')} متر | "
                f"{getattr(p, 'rooms', '?')} خواب | "
                f"محله: {district_name}"
            )

    # =================== 4) لیست فایل‌ها ===================

    def menu_list_listings(self) -> None:
        print("\n" + "-" * 40)
        print(Colors.BOLD + "📂 لیست همه فایل‌ها" + Colors.ENDC)
        print("-" * 40)
        listings = RealEstateRepository.all_listings()
        if not listings:
            print("هیچ فایلی ثبت نشده است.")
            return

        for l in listings:
            p = l.property
            label = self._prop_label(p)
            if isinstance(l, SaleListing):
                total_price = l.price_per_meter * getattr(p, "area", 0)
                print(
                    f"{Colors.OKGREEN}[فروش]{Colors.ENDC} "
                    f"id={l.id} | ملک id={p.id} | {label} | "
                    f"{getattr(p, 'area', '?')} متر | "
                    f"{getattr(p, 'rooms', '?')} خواب | "
                    f"قیمت کل: {total_price:,.0f}"
                )
            elif isinstance(l, RentListing):
                print(
                    f"{Colors.OKBLUE}[رهن/اجاره]{Colors.ENDC} "
                    f"id={l.id} | ملک id={p.id} | {label} | "
                    f"{getattr(p, 'area', '?')} متر | "
                    f"رهن: {l.deposit:,.0f} | اجاره: {l.rent:,.0f}"
                )

    # =================== 5) جستجو فروش ===================

    def menu_search_sales(self) -> None:
        print("\n" + "-" * 40)
        print(Colors.BOLD + "🔍 جستجو در فایل‌های فروش" + Colors.ENDC)
        print("-" * 40)

        district = input("محله (خالی = بدون فیلتر): ").strip() or None
        min_price = self._input_float("حداقل قیمت کل (خالی = بدون فیلتر): ", allow_empty=True)
        max_price = self._input_float("حداکثر قیمت کل (خالی): ", allow_empty=True)
        min_area = self._input_float("حداقل متراژ (خالی): ", allow_empty=True)
        max_area = self._input_float("حداکثر متراژ (خالی): ", allow_empty=True)
        min_rooms = self._input_int("حداقل خواب (خالی): ", allow_empty=True)
        max_rooms = self._input_int("حداکثر خواب (خالی): ", allow_empty=True)

        results = RealEstateRepository.search_sales(
            district=district,
            min_price=min_price,
            max_price=max_price,
            min_area=min_area,
            max_area=max_area,
            min_rooms=min_rooms,
            max_rooms=max_rooms,
        )

        if not results:
            print(Colors.WARNING + "❗ موردی یافت نشد." + Colors.ENDC)
            return

        print(Colors.OKGREEN + f"✅ {len(results)} نتیجه یافت شد:" + Colors.ENDC)
        for l in results:
            p = l.property
            label = self._prop_label(p)
            total_price = l.price_per_meter * getattr(p, "area", 0)
            print(
                f"[فروش] id={l.id} | ملک id={p.id} | {label} | "
                f"{getattr(p, 'area', '?')} متر | "
                f"{getattr(p, 'rooms', '?')} خواب | "
                f"قیمت کل: {total_price:,.0f}"
            )

    # =================== 6) جستجو رهن/اجاره ===================

    def menu_search_rents(self) -> None:
        print("\n" + "-" * 40)
        print(Colors.BOLD + "🔎 جستجو در فایل‌های رهن/اجاره" + Colors.ENDC)
        print("-" * 40)

        district = input("محله (خالی = بدون فیلتر): ").strip() or None
        min_rent = self._input_float("حداقل اجاره (خالی): ", allow_empty=True)
        max_rent = self._input_float("حداکثر اجاره (خالی): ", allow_empty=True)
        min_area = self._input_float("حداقل متراژ (خالی): ", allow_empty=True)
        max_area = self._input_float("حداکثر متراژ (خالی): ", allow_empty=True)
        min_rooms = self._input_int("حداقل خواب (خالی): ", allow_empty=True)
        max_rooms = self._input_int("حداکثر خواب (خالی): ", allow_empty=True)

        results = RealEstateRepository.search_rents(
            district=district,
            min_rent=min_rent,
            max_rent=max_rent,
            min_area=min_area,
            max_area=max_area,
            min_rooms=min_rooms,
            max_rooms=max_rooms,
        )

        if not results:
            print(Colors.WARNING + "❗ موردی یافت نشد." + Colors.ENDC)
            return

        print(Colors.OKGREEN + f"✅ {len(results)} نتیجه یافت شد:" + Colors.ENDC)
        for l in results:
            p = l.property
            label = self._prop_label(p)
            print(
                f"[رهن/اجاره] id={l.id} | ملک id={p.id} | {label} | "
                f"{getattr(p, 'area', '?')} متر | "
                f"رهن: {l.deposit:,.0f} | اجاره: {l.rent:,.0f}"
            )

    # =================== 7) حذف ملک ===================

    def menu_delete_property(self) -> None:
        print("\n" + "-" * 40)
        print(Colors.BOLD + "❌ حذف ملک" + Colors.ENDC)
        print("-" * 40)
        self.menu_list_properties(show_header=False)
        prop_id = self._input_int("id ملک برای حذف: ")
        prop = self._get_property_by_id(prop_id)
        if prop is None:
            print(Colors.FAIL + "❌ ملکی با این id پیدا نشد." + Colors.ENDC)
            return

        to_delete = [l for l in RealEstateRepository.all_listings() if l.property is prop]
        for l in to_delete:
            BaseEntity.objects_list.remove(l)

        BaseEntity.objects_list.remove(prop)
        print(
            Colors.OKGREEN
            + f"✅ ملک id={prop_id} و {len(to_delete)} فایل مرتبط حذف شد."
            + Colors.ENDC
        )

    # =================== 8) حذف فایل ===================

    def menu_delete_listing(self) -> None:
        print("\n" + "-" * 40)
        print(Colors.BOLD + "🗑 حذف فایل (Listing)" + Colors.ENDC)
        print("-" * 40)
        self.menu_list_listings()
        listing_id = self._input_int("id فایل برای حذف: ")
        listing = self._get_listing_by_id(listing_id)
        if listing is None:
            print(Colors.FAIL + "❌ فایلی با این id پیدا نشد." + Colors.ENDC)
            return

        BaseEntity.objects_list.remove(listing)
        print(Colors.OKGREEN + f"✅ فایل id={listing_id} حذف شد." + Colors.ENDC)

    # =================== 9) ویرایش ملک ===================

    def menu_update_property(self) -> None:
        print("\n" + "-" * 40)
        print(Colors.BOLD + "✏️ ویرایش اطلاعات ملک" + Colors.ENDC)
        print("-" * 40)
        self.menu_list_properties(show_header=False)
        prop_id = self._input_int("id ملک برای ویرایش: ")
        prop = self._get_property_by_id(prop_id)
        if prop is None:
            print(Colors.FAIL + "❌ ملکی با این id پیدا نشد." + Colors.ENDC)
            return

        print("برای فیلدهایی که نمی‌خواهید تغییر دهید، خالی بگذارید و Enter بزنید.\n")

        address = input(f"آدرس [{prop.address}]: ").strip() or prop.address

        area = self._input_float(f"متراژ [{getattr(prop, 'area', '?')}]: ", allow_empty=True)
        if area is None:
            area = getattr(prop, "area", None)

        rooms = self._input_int(f"تعداد خواب [{getattr(prop, 'rooms', '?')}]: ", allow_empty=True)
        if rooms is None:
            rooms = getattr(prop, "rooms", None)

        build_year = self._input_int(
            f"سال ساخت [{getattr(prop, 'build_year', '?')}]: ",
            allow_empty=True,
        )
        if build_year is None:
            build_year = getattr(prop, "build_year", None)

        old_district_name = getattr(getattr(prop, "district", None), "name", "")
        district_name = input(f"محله [{old_district_name}]: ").strip()
        if district_name:
            district = District(district_name)
        else:
            district = getattr(prop, "district", None)

        # اعمال تغییرات
        prop.address = address
        if area is not None:
            prop.area = area
        if rooms is not None:
            prop.rooms = rooms
        if build_year is not None:
            prop.build_year = build_year
        if district is not None:
            prop.district = district

        print(Colors.OKGREEN + f"✅ ملک id={prop.id} بروزرسانی شد." + Colors.ENDC)


# اجرای مستقیم سرویس

