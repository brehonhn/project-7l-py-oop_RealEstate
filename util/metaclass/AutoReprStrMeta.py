from abc import ABCMeta


class AutoReprStrMeta(ABCMeta):
    """
    متاکلاسی که به‌صورت خودکار __repr__ و __str__ بر اساس
    __repr_fields__ و __str_fields__ در کلاس‌ها تولید می‌کند.
    """

    def __new__(mcls, name, bases, namespace):
        # اگر خود کلاس __repr__ تعریف نکرده بود، براش بساز
        if "__repr__" not in namespace:
            def __repr__(self):
                parts = []
                for cls in type(self).__mro__:
                    fields = getattr(cls, "__repr_fields__", ())
                    for field in fields:
                        if hasattr(self, field):
                            value = getattr(self, field)
                            parts.append(f"{field}={value!r}")
                return f"{type(self).__name__}({', '.join(parts)})"
            namespace["__repr__"] = __repr__

        # اگر خود کلاس __str__ تعریف نکرده بود، براش بساز
        if "__str__" not in namespace:
            def __str__(self):
                parts = []
                for cls in type(self).__mro__:
                    fields = getattr(cls, "__str_fields__", ())
                    for field in fields:
                        if hasattr(self, field):
                            value = getattr(self, field)
                            parts.append(f"{field}={value}")
                return f"{type(self).__name__}({', '.join(parts)})"
            namespace["__str__"] = __str__

        return super().__new__(mcls, name, bases, namespace)
