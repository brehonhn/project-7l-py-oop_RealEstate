import tkinter as tk
from tkinter import ttk, messagebox

# import های خودت رو با ساختار پروژه‌ات تنظیم کن
from repository.RealEstateRepository import RealEstateRepository
from entity.seller.Seller import Seller
from entity.property.District import District
from entity.property.Apartment import Apartment
from entity.property.Villa import Villa
from entity.property.Shop import Shop
from entity.listing.SaleListing import SaleListing
from entity.listing.RentListing import RentListing
from util.enums.UsageType import UsageType
from entity.base.BaseEntity import BaseEntity

class RealEstateGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("سیستم مشاور املاک (Tkinter)")
        self.geometry("950x600")

        # داده نمونه
        # RealEstateRepository.seed_data()

        # تب‌ها
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.prop_frame = ttk.Frame(self.notebook)
        self.listing_frame = ttk.Frame(self.notebook)
        self.search_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.prop_frame, text="ملک‌ها")
        self.notebook.add(self.listing_frame, text="فایل‌ها")
        self.notebook.add(self.search_frame, text="جستجو")

        self._build_properties_tab()
        self._build_listings_tab()
        self._build_search_tab()

    def _prop_label(self, p) -> str:
        """متن خوانا برای نمایش ملک، بدون نیاز به title."""
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
    # =================== TAB 1: Properties ===================

    def _build_properties_tab(self):
        top_bar = ttk.Frame(self.prop_frame)
        top_bar.pack(fill="x", pady=5)

        ttk.Button(top_bar, text="➕ افزودن ملک", command=self._open_add_property_window).pack(side="left", padx=5)
        ttk.Button(top_bar, text="❌ حذف ملک انتخاب‌شده", command=self._delete_selected_property).pack(side="left", padx=5)
        ttk.Button(top_bar, text="↻ بروزرسانی لیست", command=self._load_properties).pack(side="left", padx=5)

        columns = ("id", "type", "seller", "district", "area", "rooms", "build_year", "address")
        self.prop_tree = ttk.Treeview(self.prop_frame, columns=columns, show="headings")
        for col, text in zip(columns,
                             ["ID", "نوع", "فروشنده", "محله", "متراژ", "خواب", "سال ساخت", "آدرس"]):
            self.prop_tree.heading(col, text=text)
            self.prop_tree.column(col, width=100, anchor="center")

        self.prop_tree.pack(fill="both", expand=True, padx=5, pady=5)
        self._load_properties()

    def _load_properties(self):
        for row in self.prop_tree.get_children():
            self.prop_tree.delete(row)

        for p in RealEstateRepository.all_properties():
            prop_type = type(p).__name__
            seller_name = getattr(getattr(p, "seller", None), "full_name", "")
            district_name = getattr(getattr(p, "district", None), "name", "")
            self.prop_tree.insert(
                "",
                "end",
                iid=str(p.id),
                values=(
                    p.id,
                    prop_type,
                    seller_name,
                    district_name,
                    getattr(p, "area", ""),
                    getattr(p, "rooms", ""),
                    getattr(p, "build_year", ""),
                    getattr(p, "address", ""),
                ),
            )

    def _open_add_property_window(self):
        win = tk.Toplevel(self)
        win.title("افزودن ملک جدید")
        win.geometry("400x500")

        # نوع ملک
        ttk.Label(win, text="نوع ملک:").pack(anchor="w", padx=10, pady=2)
        prop_type_var = tk.StringVar(value="Apartment")
        ttk.Radiobutton(win, text="آپارتمان", variable=prop_type_var, value="Apartment").pack(anchor="w", padx=20)
        ttk.Radiobutton(win, text="ویلا/خانه", variable=prop_type_var, value="House").pack(anchor="w", padx=20)
        ttk.Radiobutton(win, text="مغازه", variable=prop_type_var, value="Shop").pack(anchor="w", padx=20)

        # فروشنده
        seller_name_var = tk.StringVar()
        seller_phone_var = tk.StringVar()
        ttk.Label(win, text="نام فروشنده:").pack(anchor="w", padx=10, pady=2)
        ttk.Entry(win, textvariable=seller_name_var).pack(fill="x", padx=10)
        ttk.Label(win, text="تلفن فروشنده:").pack(anchor="w", padx=10, pady=2)
        ttk.Entry(win, textvariable=seller_phone_var).pack(fill="x", padx=10)

        # مشخصات ملک
        district_var = tk.StringVar()
        address_var = tk.StringVar()
        area_var = tk.StringVar()
        rooms_var = tk.StringVar()
        build_year_var = tk.StringVar()

        ttk.Label(win, text="محله:").pack(anchor="w", padx=10, pady=2)
        ttk.Entry(win, textvariable=district_var).pack(fill="x", padx=10)

        ttk.Label(win, text="آدرس:").pack(anchor="w", padx=10, pady=2)
        ttk.Entry(win, textvariable=address_var).pack(fill="x", padx=10)

        ttk.Label(win, text="متراژ (متر):").pack(anchor="w", padx=10, pady=2)
        ttk.Entry(win, textvariable=area_var).pack(fill="x", padx=10)

        ttk.Label(win, text="تعداد خواب:").pack(anchor="w", padx=10, pady=2)
        ttk.Entry(win, textvariable=rooms_var).pack(fill="x", padx=10)

        ttk.Label(win, text="سال ساخت:").pack(anchor="w", padx=10, pady=2)
        ttk.Entry(win, textvariable=build_year_var).pack(fill="x", padx=10)

        # کاربری
        usage_var = tk.StringVar(value="RESIDENTIAL")
        ttk.Label(win, text="کاربری:").pack(anchor="w", padx=10, pady=2)
        ttk.Radiobutton(win, text="مسکونی", variable=usage_var, value="RESIDENTIAL").pack(anchor="w", padx=20)
        ttk.Radiobutton(win, text="تجاری", variable=usage_var, value="COMMERCIAL").pack(anchor="w", padx=20)
        ttk.Radiobutton(win, text="اداری", variable=usage_var, value="OFFICE").pack(anchor="w", padx=20)

        # ویژگی‌های خاص آپارتمان / ویلا
        apt_elev_var = tk.BooleanVar(value=True)
        apt_park_var = tk.BooleanVar(value=True)
        apt_floor_var = tk.StringVar(value="1")

        house_yard_var = tk.BooleanVar(value=True)
        house_floors_var = tk.StringVar(value="2")

        frame_spec = ttk.LabelFrame(win, text="ویژگی‌های خاص")
        frame_spec.pack(fill="x", padx=10, pady=10)

        ttk.Checkbutton(frame_spec, text="آسانسور", variable=apt_elev_var).pack(anchor="w", padx=10)
        ttk.Checkbutton(frame_spec, text="پارکینگ", variable=apt_park_var).pack(anchor="w", padx=10)
        ttk.Label(frame_spec, text="طبقه (برای آپارتمان):").pack(anchor="w", padx=10, pady=2)
        ttk.Entry(frame_spec, textvariable=apt_floor_var).pack(fill="x", padx=10)

        ttk.Checkbutton(frame_spec, text="حیاط (برای ویلا)", variable=house_yard_var).pack(anchor="w", padx=10)
        ttk.Label(frame_spec, text="تعداد طبقات (ویلا):").pack(anchor="w", padx=10, pady=2)
        ttk.Entry(frame_spec, textvariable=house_floors_var).pack(fill="x", padx=10)

        def submit():
            try:
                seller = Seller(full_name=seller_name_var.get(), phone_number=seller_phone_var.get())
                district = District(district_var.get())
                usage = UsageType[usage_var.get()]
                area = float(area_var.get())
                rooms = int(rooms_var.get())
                build_year = int(build_year_var.get())
            except Exception as e:
                messagebox.showerror("خطا", f"ورودی نامعتبر: {e}")
                return

            if prop_type_var.get() == "Apartment":
                Apartment(
                    seller=seller,
                    area=area,
                    rooms=rooms,
                    build_year=build_year,
                    district=district,
                    address=address_var.get(),
                    have_elevator=apt_elev_var.get(),
                    have_parking=apt_park_var.get(),
                    floor=int(apt_floor_var.get() or "1"),
                    usage_type=usage,
                )
            elif prop_type_var.get() == "House":
                Villa(
                    seller=seller,
                    area=area,
                    rooms=rooms,
                    build_year=build_year,
                    district=district,
                    address=address_var.get(),
                    have_yard=house_yard_var.get(),
                    floors=int(house_floors_var.get() or "1"),
                    usage_type=usage,
                )
            else:
                Shop(
                    seller=seller,
                    area=area,
                    rooms=rooms,
                    build_year=build_year,
                    district=district,
                    address=address_var.get(),
                    usage_type=usage,
                )

            self._load_properties()
            win.destroy()
            messagebox.showinfo("موفق", "ملک با موفقیت ثبت شد.")

        ttk.Button(win, text="ثبت", command=submit).pack(pady=10)

    def _delete_selected_property(self):
        selected = self.prop_tree.selection()
        if not selected:
            messagebox.showwarning("هشدار", "هیچ ملکی انتخاب نشده است.")
            return

        prop_id = int(selected[0])
        # پیدا کردن object
        prop = None
        for p in RealEstateRepository.all_properties():
            if getattr(p, "id", None) == prop_id:
                prop = p
                break

        if prop is None:
            messagebox.showerror("خطا", "ملک در حافظه یافت نشد.")
            return

        if not messagebox.askyesno("تأیید", "همراه با ملک، همه‌ی فایل‌های مرتبط هم حذف می‌شوند. ادامه دهم؟"):
            return

        # حذف فایل‌های مرتبط
        to_delete = [l for l in RealEstateRepository.all_listings() if l.property is prop]
        for l in to_delete:
            BaseEntity.objects_list.remove(l)

        # حذف ملک
        BaseEntity.objects_list.remove(prop)
        self._load_properties()
        self._load_listings()
        messagebox.showinfo("موفق", "ملک و فایل‌های مرتبط حذف شدند.")

    # =================== TAB 2: Listings ===================

    def _build_listings_tab(self):
        top_bar = ttk.Frame(self.listing_frame)
        top_bar.pack(fill="x", pady=5)

        ttk.Button(top_bar, text="➕ افزودن فایل", command=self._open_add_listing_window).pack(side="left", padx=5)
        ttk.Button(top_bar, text="❌ حذف فایل انتخاب‌شده", command=self._delete_selected_listing).pack(side="left", padx=5)
        ttk.Button(top_bar, text="↻ بروزرسانی", command=self._load_listings).pack(side="left", padx=5)

        columns = ("id", "kind", "prop_id", "summary")
        self.listing_tree = ttk.Treeview(self.listing_frame, columns=columns, show="headings")
        self.listing_tree.heading("id", text="ID فایل")
        self.listing_tree.heading("kind", text="نوع")
        self.listing_tree.heading("prop_id", text="ID ملک")
        self.listing_tree.heading("summary", text="خلاصه")

        self.listing_tree.column("id", width=80, anchor="center")
        self.listing_tree.column("kind", width=80, anchor="center")
        self.listing_tree.column("prop_id", width=80, anchor="center")
        self.listing_tree.column("summary", width=600, anchor="w")

        self.listing_tree.pack(fill="both", expand=True, padx=5, pady=5)
        self._load_listings()

    def _load_listings(self):
        for row in self.listing_tree.get_children():
            self.listing_tree.delete(row)

        for l in RealEstateRepository.all_listings():
            p = l.property
            label = self._prop_label(p)
            if isinstance(l, SaleListing):
                kind = "فروش"
                total_price = l.price_per_meter * getattr(p, "area", 0)
                summary = f"{label} | قیمت هر متر: {l.price_per_meter:,.0f} | کل: {total_price:,.0f}"
            else:
                kind = "رهن/اجاره"
                summary = f"{label} | رهن: {l.deposit:,.0f} | اجاره: {l.rent:,.0f}"

            self.listing_tree.insert(
                "",
                "end",
                iid=str(l.id),
                values=(l.id, kind, getattr(p, "id", ""), summary),
            )

    def _open_add_listing_window(self):
        win = tk.Toplevel(self)
        win.title("افزودن فایل جدید")
        win.geometry("400x350")

        # انتخاب ملک
        ttk.Label(win, text="ID ملک:").pack(anchor="w", padx=10, pady=2)
        prop_id_var = tk.StringVar()
        ttk.Entry(win, textvariable=prop_id_var).pack(fill="x", padx=10)
        ttk.Label(win, text="(برای دیدن لیست ID ها، به تب ملک‌ها بروید)").pack(anchor="w", padx=10, pady=2)

        # نوع فایل
        kind_var = tk.StringVar(value="SALE")
        ttk.Label(win, text="نوع فایل:").pack(anchor="w", padx=10, pady=2)
        ttk.Radiobutton(win, text="فروش", variable=kind_var, value="SALE").pack(anchor="w", padx=20)
        ttk.Radiobutton(win, text="رهن/اجاره", variable=kind_var, value="RENT").pack(anchor="w", padx=20)

        price_per_meter_var = tk.StringVar()
        discount_var = tk.StringVar(value="0")
        swap_var = tk.BooleanVar(value=False)

        deposit_var = tk.StringVar()
        rent_var = tk.StringVar()
        convertible_var = tk.BooleanVar(value=False)

        frame_sale = ttk.LabelFrame(win, text="فروش")
        frame_rent = ttk.LabelFrame(win, text="رهن/اجاره")
        frame_sale.pack(fill="x", padx=10, pady=5)
        frame_rent.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_sale, text="قیمت هر متر:").pack(anchor="w", padx=10, pady=2)
        ttk.Entry(frame_sale, textvariable=price_per_meter_var).pack(fill="x", padx=10)
        ttk.Label(frame_sale, text="تخفیف (%):").pack(anchor="w", padx=10, pady=2)
        ttk.Entry(frame_sale, textvariable=discount_var).pack(fill="x", padx=10)
        ttk.Checkbutton(frame_sale, text="قابل معاوضه", variable=swap_var).pack(anchor="w", padx=10, pady=2)

        ttk.Label(frame_rent, text="رهن:").pack(anchor="w", padx=10, pady=2)
        ttk.Entry(frame_rent, textvariable=deposit_var).pack(fill="x", padx=10)
        ttk.Label(frame_rent, text="اجاره:").pack(anchor="w", padx=10, pady=2)
        ttk.Entry(frame_rent, textvariable=rent_var).pack(fill="x", padx=10)
        ttk.Checkbutton(frame_rent, text="قابل تبدیل", variable=convertible_var).pack(anchor="w", padx=10, pady=2)

        def submit():
            try:
                prop_id = int(prop_id_var.get())
            except ValueError:
                messagebox.showerror("خطا", "ID ملک باید عدد باشد.")
                return

            prop = None
            for p in RealEstateRepository.all_properties():
                if getattr(p, "id", None) == prop_id:
                    prop = p
                    break
            if prop is None:
                messagebox.showerror("خطا", "ملک با این ID پیدا نشد.")
                return

            if kind_var.get() == "SALE":
                try:
                    price = float(price_per_meter_var.get())
                    discount = float(discount_var.get() or "0")
                except ValueError:
                    messagebox.showerror("خطا", "قیمت/تخفیف نامعتبر است.")
                    return
                SaleListing(
                    prop=prop,
                    price_per_meter=price,
                    discount=discount,
                    swap=swap_var.get(),
                )
            else:
                try:
                    deposit = float(deposit_var.get())
                    rent = float(rent_var.get())
                except ValueError:
                    messagebox.showerror("خطا", "رهن/اجاره نامعتبر است.")
                    return
                RentListing(
                    prop=prop,
                    deposit=deposit,
                    rent=rent,
                    convertible=convertible_var.get(),
                    discount=0.0,
                )

            self._load_listings()
            win.destroy()
            messagebox.showinfo("موفق", "فایل با موفقیت ثبت شد.")

        ttk.Button(win, text="ثبت", command=submit).pack(pady=10)

    def _delete_selected_listing(self):
        selected = self.listing_tree.selection()
        if not selected:
            messagebox.showwarning("هشدار", "هیچ فایلی انتخاب نشده است.")
            return
        listing_id = int(selected[0])

        listing = None
        for l in RealEstateRepository.all_listings():
            if getattr(l, "id", None) == listing_id:
                listing = l
                break

        if listing is None:
            messagebox.showerror("خطا", "فایل در حافظه یافت نشد.")
            return

        if not messagebox.askyesno("تأیید", "آیا از حذف این فایل مطمئن هستید؟"):
            return

        BaseEntity.objects_list.remove(listing)
        self._load_listings()
        messagebox.showinfo("موفق", "فایل حذف شد.")

    # =================== TAB 3: Search ===================

    def _build_search_tab(self):
        frame_top = ttk.Frame(self.search_frame)
        frame_top.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_top, text="نوع جستجو:").grid(row=0, column=0, sticky="w")
        self.search_kind_var = tk.StringVar(value="SALE")
        ttk.Radiobutton(frame_top, text="فروش", variable=self.search_kind_var, value="SALE").grid(row=0, column=1, sticky="w")
        ttk.Radiobutton(frame_top, text="رهن/اجاره", variable=self.search_kind_var, value="RENT").grid(row=0, column=2, sticky="w")

        # فیلدهای مشترک
        self.search_district_var = tk.StringVar()
        self.search_min_area_var = tk.StringVar()
        self.search_max_area_var = tk.StringVar()
        self.search_min_rooms_var = tk.StringVar()
        self.search_max_rooms_var = tk.StringVar()
        self.search_min_price_var = tk.StringVar()
        self.search_max_price_var = tk.StringVar()

        row = 1
        ttk.Label(frame_top, text="محله:").grid(row=row, column=0, sticky="w", pady=2)
        ttk.Entry(frame_top, textvariable=self.search_district_var, width=20).grid(row=row, column=1, sticky="w")

        row += 1
        ttk.Label(frame_top, text="حداقل متراژ:").grid(row=row, column=0, sticky="w", pady=2)
        ttk.Entry(frame_top, textvariable=self.search_min_area_var, width=10).grid(row=row, column=1, sticky="w")
        ttk.Label(frame_top, text="حداکثر متراژ:").grid(row=row, column=2, sticky="w", pady=2)
        ttk.Entry(frame_top, textvariable=self.search_max_area_var, width=10).grid(row=row, column=3, sticky="w")

        row += 1
        ttk.Label(frame_top, text="حداقل خواب:").grid(row=row, column=0, sticky="w", pady=2)
        ttk.Entry(frame_top, textvariable=self.search_min_rooms_var, width=10).grid(row=row, column=1, sticky="w")
        ttk.Label(frame_top, text="حداکثر خواب:").grid(row=row, column=2, sticky="w", pady=2)
        ttk.Entry(frame_top, textvariable=self.search_max_rooms_var, width=10).grid(row=row, column=3, sticky="w")

        row += 1
        ttk.Label(frame_top, text="حداقل قیمت/اجاره:").grid(row=row, column=0, sticky="w", pady=2)
        ttk.Entry(frame_top, textvariable=self.search_min_price_var, width=10).grid(row=row, column=1, sticky="w")
        ttk.Label(frame_top, text="حداکثر قیمت/اجاره:").grid(row=row, column=2, sticky="w", pady=2)
        ttk.Entry(frame_top, textvariable=self.search_max_price_var, width=10).grid(row=row, column=3, sticky="w")

        row += 1
        ttk.Button(frame_top, text="🔍 جستجو", command=self._do_search).grid(row=row, column=0, pady=5)

        # جدول نتایج
        columns = ("kind", "prop", "summary")
        self.search_tree = ttk.Treeview(self.search_frame, columns=columns, show="headings")
        self.search_tree.heading("kind", text="نوع")
        self.search_tree.heading("prop", text="ملک")
        self.search_tree.heading("summary", text="خلاصه")
        self.search_tree.column("kind", width=80, anchor="center")
        self.search_tree.column("prop", width=200, anchor="w")
        self.search_tree.column("summary", width=600, anchor="w")
        self.search_tree.pack(fill="both", expand=True, padx=10, pady=10)

    def _do_search(self):
        # تبدیل ورودی‌ها
        district = self.search_district_var.get().strip() or None

        def safe_float(s):
            s = s.strip()
            return float(s) if s else None

        def safe_int(s):
            s = s.strip()
            return int(s) if s else None

        min_area = safe_float(self.search_min_area_var.get())
        max_area = safe_float(self.search_max_area_var.get())
        min_rooms = safe_int(self.search_min_rooms_var.get())
        max_rooms = safe_int(self.search_max_rooms_var.get())
        min_price = safe_float(self.search_min_price_var.get())
        max_price = safe_float(self.search_max_price_var.get())

        for row in self.search_tree.get_children():
            self.search_tree.delete(row)

        if self.search_kind_var.get() == "SALE":
            results = RealEstateRepository.search_sales(
                district=district,
                min_price=min_price,
                max_price=max_price,
                min_area=min_area,
                max_area=max_area,
                min_rooms=min_rooms,
                max_rooms=max_rooms,
            )
            for l in results:
                p = l.property
                label = self._prop_label(p)
                total_price = l.price_per_meter * getattr(p, "area", 0)
                summary = f"{getattr(p, 'area', '?')}متر | {getattr(p, 'rooms', '?')}خواب | کل: {total_price:,.0f}"
                self.search_tree.insert("", "end", values=("فروش", label, summary))
        else:
            results = RealEstateRepository.search_rents(
                district=district,
                min_rent=min_price,
                max_rent=max_price,
                min_area=min_area,
                max_area=max_area,
                min_rooms=min_rooms,
                max_rooms=max_rooms,
            )
            for l in results:
                p = l.property
                label = self._prop_label(p)
                summary = f"{getattr(p, 'area', '?')}متر | رهن: {l.deposit:,.0f} | اجاره: {l.rent:,.0f}"
                self.search_tree.insert("", "end", values=("رهن/اجاره", label, summary))



