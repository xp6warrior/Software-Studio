from enum import Enum

class StatusEnum(Enum):
    LOST = "lost"
    FOUND = "found"

class SizeEnum(Enum):
    XS = "xs"
    S = "s"
    M = "m"
    L = "l"
    XL = "xl"

class ColorEnum(Enum):
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

class MaterialEnum(Enum):
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

class PersonalItemType(Enum):
    ID_CARD = "id_card"
    PASSPORT = "passport"
    KEYS = "keys"
    CREDIT_CARD = "credit_card"
    OTHER = "other"

class JewelryType(Enum):
    RING = "ring"
    EARRINGS = "earrings"
    NECKLACE = "necklace"
    PIERCING = "piercing"
    OTHER = "other"

class AccessoryType(Enum):
    GLASSES = "glasses"
    SUNGLASSES = "sunglasses"
    WRISTWATCH = "wristwatch"
    OTHER = "other"

class TravelItemType(Enum):
    SUITCASE = "suitcase"
    HANDBAG = "handbag"
    BACKPACK = "backpack"
    LUGGAGE = "luggage"
    UMBRELLA = "umbrella"
    WALLET = "wallet"
    PURSE = "purse"
    WATER_BOTTLE = "water_bottle"
    OTHER = "other"

class ElectronicDeviceType(Enum):
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

class ClothingType(Enum):
    COAT = "coat"
    JACKET = "jacket"
    GLOVES = "gloves"
    SCARF = "scarf"
    HAT = "hat"
    SHOES = "shoes"
    OTHER = "other"

class OfficeItemType(Enum):
    PEN = "pen"
    FOLDER = "folder"
    BOOK = "book"
    OTHER = "other"