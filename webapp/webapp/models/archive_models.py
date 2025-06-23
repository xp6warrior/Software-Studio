import reflex as rx
from sqlmodel import Field
from . import enums as e
from datetime import datetime

# TODO find a better way to define these classes

class ArchivePersonalItems(rx.Model, table=True):
    __tablename__ = "personalitems"
    __table_args__ = {"schema": "archive"}

    id: int = Field(primary_key=True)
    type: e.PersonalItemType = e.enum_field(e.PersonalItemType, "PersonalItemType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    description: str
    time_stamp: datetime

    email: str
    username: str
    surname: str
    pesel: int = Field(unique=True, nullable=False)

class ArchiveJewelry(rx.Model, table=True):
    __tablename__ = "jewelry"
    __table_args__ = {"schema": "archive"}

    id: int = Field(primary_key=True)
    type: e.JewelryType = e.enum_field(e.JewelryType, "JewelryType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = e.enum_field(e.SizeEnum, "SizeEnum")
    description: str
    time_stamp: datetime

    email: str
    username: str
    surname: str
    pesel: int = Field(unique=True, nullable=False)

class ArchiveAccessories(rx.Model, table=True):
    __tablename__ = "accessories"
    __table_args__ = {"schema": "archive"}

    id: int = Field(primary_key=True)
    type: e.AccessoryType = e.enum_field(e.AccessoryType, "AccessoryType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    time_stamp: datetime

    email: str
    username: str
    surname: str
    pesel: int = Field(unique=True, nullable=False)

class ArchiveTravelItems(rx.Model, table=True):
    __tablename__ = "travelitems"
    __table_args__ = {"schema": "archive"}

    id: int = Field(primary_key=True)
    type: e.TravelItemType = e.enum_field(e.TravelItemType, "TravelItemType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = e.enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    time_stamp: datetime

    email: str
    username: str
    surname: str
    pesel: int = Field(unique=True, nullable=False)

class ArchiveElectronicDevices(rx.Model, table=True):
    __tablename__ = "electronicdevices"
    __table_args__ = {"schema": "archive"}

    id: int = Field(primary_key=True)
    type: e.ElectronicDeviceType = e.enum_field(e.ElectronicDeviceType, "ElectronicDeviceType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    time_stamp: datetime

    email: str
    username: str
    surname: str
    pesel: int = Field(unique=True, nullable=False)

class ArchiveClothing(rx.Model, table=True):
    __tablename__ = "clothing"
    __table_args__ = {"schema": "archive"}

    id: int = Field(primary_key=True)
    type: e.ClothingType = e.enum_field(e.ClothingType, "ClothingType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = e.enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    time_stamp: datetime

    email: str
    username: str
    surname: str
    pesel: int = Field(unique=True, nullable=False)

class ArchiveOfficeItems(rx.Model, table=True):
    __tablename__ = "officeitems"
    __table_args__ = {"schema": "archive"}

    id: int = Field(primary_key=True)
    type: e.OfficeItemType = e.enum_field(e.OfficeItemType, "OfficeItemType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = e.enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    name: str
    description: str
    time_stamp: datetime

    email: str
    username: str
    surname: str
    pesel: int = Field(unique=True, nullable=False)

class ArchiveOtherItems(rx.Model, table=True):
    __tablename__ = "otheritems"
    __table_args__ = {"schema": "archive"}

    id: int = Field(primary_key=True)
    type: str
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = e.enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    name: str
    description: str
    time_stamp: datetime

    email: str
    username: str
    surname: str
    pesel: int = Field(unique=True, nullable=False)