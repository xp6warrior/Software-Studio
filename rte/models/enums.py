from enum import Enum as PyEnum
from sqlalchemy import Column, Enum as dbEnum

def enum_field(enum_cls, enum_name):
    return Column(dbEnum(
        enum_cls,
        name=enum_name,
        create_type=False,
        native_enum=False,
        values_callable=lambda x: [e.value for e in x]
    ), nullable=False)

class RoleEnum(str, PyEnum):
    USER = "user"
    WORKER = "worker"
    ADMIN = "admin"

class StatusEnum(str, PyEnum):
    LOST = "lost"
    FOUND = "found"

class SizeEnum(str, PyEnum):
    XS = "xs"
    S = "s"
    M = "m"
    L = "l"
    XL = "xl"

class ColorEnum(str, PyEnum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"
    ORANGE = "orange"
    PURPLE = "purple"
    PINK = "pink"
    BROWN = "brown"
    BLACK = "black"
    WHITE = "white"
    GRAY = "gray"
    CYAN = "cyan"
    MAROON = "maroon"
    NAVY = "navy"
    BEIGE = "beige"
    OTHER = "other"

class MaterialEnum(str, PyEnum):
    WOOD = "wood"
    METAL = "metal"
    PLASTIC = "plastic"
    GLASS = "glass"
    CERAMIC = "ceramic"
    FABRIC = "fabric"
    LEATHER = "leather"
    RUBBER = "rubber"
    PAPER = "paper"
    OTHER = "other"

class PersonalItemType(str, PyEnum):
    ID_CARD = "id_card"
    PASSPORT = "passport"
    KEYS = "keys"
    CREDIT_DEBIT_CARD = "credit_debit_card"
    OTHER = "other"

class JewelryType(str, PyEnum):
    RING = "ring"
    EARRINGS = "earrings"
    NECKLACE = "necklace"
    PIERCING = "piercing"
    OTHER = "other"

class AccessoryType(str, PyEnum):
    GLASSES = "glasses"
    SUNGLASSES = "sunglasses"
    WRISTWATCH = "wristwatch"
    OTHER = "other"

class TravelItemType(str, PyEnum):
    SUITCASE = "suitcase"
    HANDBAG = "handbag"
    BACKPACK = "backpack"
    LUGGAGE = "luggage"
    UMBRELLA = "umbrella"
    WALLET = "wallet"
    PURSE = "purse"
    WATER_BOTTLE = "water_bottle"
    OTHER = "other"

class ElectronicDeviceType(str, PyEnum):
    PHONE = "phone"
    LAPTOP = "laptop"
    TABLET = "tablet"
    CABLE = "cable"
    EARBUDS = "earbuds"
    HEADPHONES = "headphones"
    CAMERA = "camera"
    SMARTWATCH = "smartwatch"
    POWERBANK = "powerbank"
    OTHER = "other"

class ClothingType(str, PyEnum):
    COAT = "coat"
    JACKET = "jacket"
    GLOVES = "gloves"
    SCARF = "scarf"
    HAT = "hat"
    SHOES = "shoes"
    OTHER = "other"

class OfficeItemType(str, PyEnum):
    PEN = "pen"
    FOLDER = "folder"
    BOOK = "book"
    OTHER = "other"

class MatchStatus(str, PyEnum):
    UNCONFIRMED = "unconfirmed"
    CONFIRMED = "confirmed"
    DECLINED = "declined"
