from enum import Enum


class Gender(str, Enum):
    FEMALE = "Female"
    MALE = "Male"
    UNKNOWN = "Unknown"
