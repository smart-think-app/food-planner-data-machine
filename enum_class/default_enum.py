import enum


class DefaultEnumMeta(enum.EnumMeta):
    default = object()

    def __call__(cls, value=default, *args, **kwargs):
        if value is DefaultEnumMeta.default:
            # Assume the first enum_class is default
            return next(iter(cls))
        return super().__call__(value, *args, **kwargs)