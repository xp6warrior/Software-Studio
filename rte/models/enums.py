from enum import Enum

class CategoryEnum(str, Enum):
    PERSONAL_ITEMS = "personal_items"
    JEWELRY = "jewelry"
    ACCESSORIES = "accessories"
    TRAVEL_ITEMS = "travel_items"
    ELECTRONIC_DEVICES = "electronic_devices"
    CLOTHING = "clothing"
    OFFICE_ITEMS = "office_items"
    OTHER_ITEMS = "other_items"

class RoleEnum(str, Enum):
    USER = "user"
    WORKER = "worker"
    ADMIN = "admin"

class StatusEnum(str, Enum):
    LOST = "lost"
    FOUND = "found"

class SizeEnum(str, Enum):
    XS = "xs"
    S = "s"
    M = "m"
    L = "l"
    XL = "xl"

class ColorEnum(str, Enum):
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

class MaterialEnum(str, Enum):
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

class PersonalItemType(str, Enum):
    ID_CARD = "id_card"
    PASSPORT = "passport"
    KEYS = "keys"
    CREDIT_DEBIT_CARD = "credit_debit_card"
    OTHER = "other"

class JewelryType(str, Enum):
    RING = "ring"
    EARRINGS = "earrings"
    NECKLACE = "necklace"
    PIERCING = "piercing"
    OTHER = "other"

class AccessoryType(str, Enum):
    GLASSES = "glasses"
    SUNGLASSES = "sunglasses"
    WRISTWATCH = "wristwatch"
    OTHER = "other"

class TravelItemType(str, Enum):
    SUITCASE = "suitcase"
    HANDBAG = "handbag"
    BACKPACK = "backpack"
    LUGGAGE = "luggage"
    UMBRELLA = "umbrella"
    WALLET = "wallet"
    PURSE = "purse"
    WATER_BOTTLE = "water_bottle"
    OTHER = "other"

class ElectronicDeviceType(str, Enum):
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

class ClothingType(str, Enum):
    COAT = "coat"
    JACKET = "jacket"
    GLOVES = "gloves"
    SCARF = "scarf"
    HAT = "hat"
    SHOES = "shoes"
    OTHER = "other"

class OfficeItemType(str, Enum):
    PEN = "pen"
    FOLDER = "folder"
    BOOK = "book"
    OTHER = "other"

class MatchStatusEnum(str, Enum):
    UNCONFIRMED = "unconfirmed"
    CONFIRMED = "confirmed"
    DECLINED = "declined"
    PICKED_UP = "picked_up"
    FALSE_PICKUP = "false_pickup"
