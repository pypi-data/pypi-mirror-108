from enum import Enum as _Enum


class Enum(_Enum):

    @classmethod
    def names(cls):
        return cls._member_names_

    @classmethod
    def values(cls):
        return [e.value for e in cls]
