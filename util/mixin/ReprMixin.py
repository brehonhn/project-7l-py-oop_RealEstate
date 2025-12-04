class ReprMixin:
    """
    Mixin عمومی برای ساخت خودکار __repr__ براساس __repr_fields__ در هر کلاس.
    هر کلاس در زنجیرهٔ ارث‌بری می‌تواند __repr_fields__ تعریف کند.
    """

    __repr_fields__ = ()  # کلاس‌های فرزند می‌توانند override کنند

    def __repr__(self):
        parts = []

        # روی کل سلسله‌مراتب (MRO) حرکت کن
        for cls in type(self).__mro__:
            fields = getattr(cls, "__repr_fields__", ())
            for name in fields:
                # اگر attribute وجود نداشت، رد شو
                if not hasattr(self, name):
                    continue
                value = getattr(self, name)
                parts.append(f"{name}={value!r}")

        fields_str = ", ".join(parts)
        return f"{self.__class__.__name__}({fields_str})"
