from enum import Enum


class InternetServiceOption(str, Enum):
    DSL = "DSL"
    FIBER = "Fiber optic"
    NONE = "No"
