from enum import Enum

class CategoryEnum(str, Enum):
    PERSONAL_ITEMS = "Personal Items"
    JEWELRY = "Jewelry"
    ACCESSORIES = "Accessories"
    TRAVEL_ITEMS = "Travel Items"
    ELECTRONIC_DEVICES = "Electronic Devices"
    CLOTHING = "Clothing"
    OFFICE_ITEMS = "Office Items"
    OTHER_ITEMS = "Other Items"

class RoleEnum(str, Enum):
    USER = "USER"
    WORKER = "WORKER"
    ADMIN = "ADMIN"

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
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    YELLOW = "Yellow"
    ORANGE = "Orange"
    PURPLE = "Purple"
    PINK = "Pink"
    BROWN = "Brown"
    BLACK = "Black"
    WHITE = "White"
    GRAY = "Gray"
    CYAN = "Cyan"
    MAROON = "Maroon"
    NAVY = "Navy"
    BEIGE = "Beige"
    OTHER = "Other"

class MaterialEnum(str, Enum):
    WOOD = "Wood"
    METAL = "Metal"
    PLASTIC = "Plastic"
    GLASS = "Glass"
    CERAMIC = "Ceramic"
    FABRIC = "Fabric"
    LEATHER = "Leather"
    RUBBER = "Rubber"
    PAPER = "Paper"
    OTHER = "Other"

class PersonalItemType(str, Enum):
    ID_CARD = "ID Card"
    PASSPORT = "Passport"
    KEYS = "Keys"
    CREDIT_DEBIT_CARD = "Credit/Debit Card"
    OTHER = "Other"

class JewelryType(str, Enum):
    RING = "Ring"
    EARRINGS = "Earrings"
    NECKLACE = "Necklace"
    PIERCING = "Piercing"
    OTHER = "Other"

class AccessoryType(str, Enum):
    GLASSES = "Glasses"
    SUNGLASSES = "Sunglasses"
    WRISTWATCH = "Wristwatch"
    OTHER = "Other"

class TravelItemType(str, Enum):
    SUITCASE = "Suitcase"
    HANDBAG = "Handbag"
    BACKPACK = "Backpack"
    LUGGAGE = "Luggage"
    UMBRELLA = "Umbrella"
    WALLET = "Wallet"
    PURSE = "Purse"
    WATER_BOTTLE = "Water Bottle"
    OTHER = "Other"

class ElectronicDeviceType(str, Enum):
    PHONE = "Phone"
    LAPTOP = "Laptop"
    TABLET = "Tablet"
    CABLE = "Cable"
    EARBUDS = "Earbuds"
    HEADPHONES = "Headphones"
    CAMERA = "Camera"
    SMARTWATCH = "Smartwatch"
    POWERBANK = "Powerbank"
    OTHER = "Other"

class ClothingType(str, Enum):
    COAT = "Coat"
    JACKET = "Jacket"
    GLOVES = "Gloves"
    SCARF = "Scarf"
    HAT = "Hat"
    SHOES = "Shoes"
    OTHER = "Other"

class OfficeItemType(str, Enum):
    PEN = "Pen"
    FOLDER = "Folder"
    BOOK = "Book"
    OTHER = "Other"

class MatchStatusEnum(str, Enum):
    UNCONFIRMED = "unconfirmed"
    CONFIRMED = "confirmed"
    DECLINED = "declined"
    PICKED_UP = "picked_up"
    FALSE_PICKUP = "false_pickup"
