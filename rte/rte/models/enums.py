from enum import Enum
from sqlalchemy import Column, Enum as dbEnum
from sqlmodel import Field

def enum_field(enum_cls, enum_name):
    return Field(
        sa_column = Column(dbEnum(
            enum_cls,
            name=enum_name,
            create_type=False,
            native_enum=False,
            values_callable=lambda x: [e.value for e in x]
        ), nullable=False)
    )

class ModelsEnum(str, enum.Enum):
    PERSONAL_ITEM = "personal_items"
    JEWELRY = "jewelry"
    ACCESSORIES = "accessories"
    TRAVEL_ITEMS = "travel_items"
    ELECTRONIC_DEVICES = "electronic_devices"
    CLOTHING = "clothing"
    OFFICE_ITEMS = "office_items"
    OTHER_ITEMS = "other_items"

class RoleEnum(str, enum.Enum):
    USER = "user"
    WORKER = "worker"
    ADMIN = "admin"

class StatusEnum(str, enum.Enum):
    LOST = "lost"
    FOUND = "found"
    CONFIRMED = "confirmed"

class SizeEnum(Enum):
    XS = "xs"
    S = "s"
    M = "m"
    L = "l"
    XL = "xl"

class ColorEnum(str, enum.Enum):
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

class MaterialEnum(str, enum.Enum):
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

class PersonalItemType(str, enum.Enum):
    ID_CARD = "id_card"
    PASSPORT = "passport"
    KEYS = "keys"
    CREDIT_DEBIT_CARD = "credit_debit_card"
    OTHER = "other"

class JewelryType(str, enum.Enum):
    RING = "ring"
    EARRINGS = "earrings"
    NECKLACE = "necklace"
    PIERCING = "piercing"
    OTHER = "other"

class AccessoryType(str, enum.Enum):
    GLASSES = "glasses"
    SUNGLASSES = "sunglasses"
    WRISTWATCH = "wristwatch"
    OTHER = "other"

class TravelItemType(str, enum.Enum):
    SUITCASE = "suitcase"
    HANDBAG = "handbag"
    BACKPACK = "backpack"
    LUGGAGE = "luggage"
    UMBRELLA = "umbrella"
    WALLET = "wallet"
    PURSE = "purse"
    WATER_BOTTLE = "water_bottle"
    OTHER = "other"

class ElectronicDeviceType(str, enum.Enum):
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

class ClothingType(str, enum.Enum):
    COAT = "coat"
    JACKET = "jacket"
    GLOVES = "gloves"
    SCARF = "scarf"
    HAT = "hat"
    SHOES = "shoes"
    OTHER = "other"

class OfficeItemType(str, enum.Enum):
    PEN = "pen"
    FOLDER = "folder"
    BOOK = "book"
    OTHER = "other"

class MatchStatus(str, enum.Enum):
    UNCONFIRMED = "unconfirmed"
    CONFIRMED = "confirmed"
