from enum import Enum


class Outreach(str, Enum):
    NOT_CONTACTED = "Not Contacted"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"