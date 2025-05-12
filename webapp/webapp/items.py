from dataclasses import dataclass

@dataclass
class Item:
    category : str
    item_type : str
    color : str
    desc : str
    size : str
    material : str
    brand : str
    name : str

@dataclass
class Lost_Item(Item):
    status : str
    item_id : str

@dataclass
class Found_Item(Item):
    item_id : str

@dataclass
class Matched_Item(Item):
    item_id : str
    pesel : str