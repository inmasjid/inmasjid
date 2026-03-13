from enum import Enum


class UserStoreRole(str, Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"

class OTPStatus(str, Enum):
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    EXPIRED = "EXPIRED"
    CANCELED = "CANCELED"

# Campaigns and Creatives
class CampaignStatus(str, Enum):
    DRAFT = "DRAFT"
    PENDING_REVIEW = "PENDING_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    PAUSED = "PAUSED"
    ENDED = "ENDED"


class CampaignType(str, Enum):
    PERSONAL = "PERSONAL"
    TEAM = "TEAM"


class CreativeType(str, Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"


# Payments In and Out
class PaymentMethod(str, Enum):
    UPI = "UPI"
    BANK_TRANSFER = "BANK_TRANSFER"
    CASH = "CASH"
    CARD = "CARD"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
