from enum import StrEnum


class MailingStatus(StrEnum):
    CREATED = "created"
    PROCESSED = "processed"
    FINALIZED = "finalized"
    STOPPED = "stopped"

    