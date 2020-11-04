from enum import Enum

# class Roles(enum.IntEnum):
class Roles(Enum):
    ADMIN = 0
    MANAGER = 1
    USER = 2

    def __str__(self):
        return self.name

    @classmethod
    def choices(cls):
        return [(choice, choice.value) for choice in cls]

    @classmethod
    def coerce(cls, item):
        item = cls(item) \
               if not isinstance(item, cls) \
               else item  # a ValueError thrown if item is not defined in cls.
        return item.value