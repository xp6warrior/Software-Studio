import reflex as rx
from sqlmodel import Field
from . import enums as e
import datetime

class Accounts(rx.Model, table=True):
    __tablename__ = "accounts"
    __table_args__ = {"schema": "accounts"}

    email: str = Field(primary_key=True)
    password: str
    role: e.RoleEnum = e.enum_field(e.RoleEnum, "RoleEnum")
    pesel: int = Field(nullable=False, unique=True)
    name: str
    surname: str


class PersonalItems(rx.Model, table=True):
    __tablename__ = "personalitems"
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: e.PersonalItemType = e.enum_field(e.PersonalItemType, "PersonalItemType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")
    time_stamp: datetime.datetime
    
    email : str = Field(foreign_key="accounts.accounts.email")

class Jewelry(rx.Model, table=True):
    __tablename__ = "jewelry"
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: e.JewelryType = e.enum_field(e.JewelryType, "JewelryType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = e.enum_field(e.SizeEnum, "SizeEnum")
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")
    time_stamp: datetime.datetime

    email: str = Field(foreign_key="accounts.accounts.email")

class Accessories(rx.Model, table=True):
    __tablename__ = "accessories"
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: e.AccessoryType = e.enum_field(e.AccessoryType, "AccessoryType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")
    time_stamp: datetime.datetime

    email: str = Field(foreign_key="accounts.accounts.email")

class TravelItems(rx.Model, table=True):
    __tablename__ = "travelitems"
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: e.TravelItemType = e.enum_field(e.TravelItemType, "TravelItemType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = e.enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")
    time_stamp: datetime.datetime

    email: str = Field(foreign_key="accounts.accounts.email")

class ElectronicDevices(rx.Model, table=True):
    __tablename__ = "electronicdevices"
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: e.ElectronicDeviceType = e.enum_field(e.ElectronicDeviceType, "ElectronicDeviceType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")
    time_stamp: datetime.datetime

    email: str = Field(foreign_key="accounts.accounts.email")

class Clothing(rx.Model, table=True):
    __tablename__ = "clothing"
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: e.ClothingType = e.enum_field(e.ClothingType, "ClothingType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = e.enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")
    time_stamp: datetime.datetime

    email: str = Field(foreign_key="accounts.accounts.email")

class OfficeItems(rx.Model, table=True):
    __tablename__ = "officeitems"
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: e.OfficeItemType = e.enum_field(e.OfficeItemType, "OfficeItemType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = e.enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    name: str
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")
    time_stamp: datetime.datetime

    email: str = Field(foreign_key="accounts.accounts.email")

class OtherItems(rx.Model, table=True):
    __tablename__ = "otheritems"
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: str
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = e.enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    name: str
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")
    time_stamp: datetime.datetime

    email: str = Field(foreign_key="accounts.accounts.email")

class Match(rx.Model, table=True):
    __tablename__ = "match"
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    table_name: str
    lost_item_id: int
    found_item_id: int
    status: e.MatchStatus = e.enum_field(e.MatchStatus, "MatchStatus")
    percentage: int
