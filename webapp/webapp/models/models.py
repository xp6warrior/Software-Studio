import reflex as rx
import enums as e
from sqlmodel import Field
from sqlalchemy import Column, Enum

def enum_field(enum_cls, enum_name):
    return Field(
        sa_column = Column(Enum(enum_cls, name=enum_name, create_type=False)),
        nullable = False
    )

class PersonalItems(rx.Model, table=True):
    __table_args__ = {"schema": "Lost_Found"}

    id: int = Field(primary_key=True)
    type: e.PersonalItemType = enum_field(e.PersonalItemType, "PersonalItemType")
    color: e.ColorEnum = enum_field(e.ColorEnum, "ColorEnum")
    description: str
    status: e.StatusEnum = enum_field(e.StatusEnum, "StatusEnum")

class Jewelery(rx.Model, table=True):
    __table_args__ = {"schema": "Lost_Found"}

    id: int = Field(primary_key=True)
    type: e.JewelryType = enum_field(e.JewelryType, "JewelryType")
    color: e.ColorEnum = enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = enum_field(e.SizeEnum, "SizeEnum")
    description: str
    status: e.StatusEnum = enum_field(e.StatusEnum, "StatusEnum")

class Accessories(rx.Model, table=True):
    __table_args__ = {"schema": "Lost_Found"}

    id: int = Field(primary_key=True)
    type: e.AccessoryType = enum_field(e.AccessoryType, "AccessoryType")
    color: e.ColorEnum = enum_field(e.ColorEnum, "ColorEnum")
    material: e.MaterialEnum = enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    status: e.StatusEnum = enum_field(e.StatusEnum, "StatusEnum")

class TravelItems(rx.Model, table=True):
    __table_args__ = {"schema": "Lost_Found"}

    id: int = Field(primary_key=True)
    type: e.TravelItemType = enum_field(e.TravelItemType, "TravelItemType")
    color: e.ColorEnum = enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    status: e.StatusEnum = enum_field(e.StatusEnum, "StatusEnum")

class ElectronicDevices(rx.Model, table=True):
    __table_args__ = {"schema": "Lost_Found"}

    id: int = Field(primary_key=True)
    type: e.ElectronicDeviceType = enum_field(e.ElectronicDeviceType, "ElectronicDeviceType")
    color: e.ColorEnum = enum_field(e.ColorEnum, "ColorEnum")
    material: e.MaterialEnum = enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    status: e.StatusEnum = enum_field(e.StatusEnum, "StatusEnum")

class Clothing(rx.Model, table=True):
    __table_args__ = {"schema": "Lost_Found"}

    id: int = Field(primary_key=True)
    type: e.ClothingType = enum_field(e.ClothingType, "ClothingType")
    color: e.ColorEnum = enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    status: e.StatusEnum = enum_field(e.StatusEnum, "StatusEnum")

class OfficeItems(rx.Model, table=True):
    __table_args__ = {"schema": "Lost_Found"}

    id: int = Field(primary_key=True)
    type: e.OfficeItemType = enum_field(e.OfficeItemType, "OfficeItemType")
    color: e.ColorEnum = enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = enum_field(e.MaterialEnum, "MaterialEnum")
    name: str
    description: str
    status: e.StatusEnum = enum_field(e.StatusEnum, "StatusEnum")

class OtherItems(rx.Model, table=True):
    __table_args__ = {"schema": "Lost_Found"}

    id: int = Field(primary_key=True)
    type: str
    color: e.ColorEnum = enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    name: str
    description: str
    status: e.StatusEnum = enum_field(e.StatusEnum, "StatusEnum")