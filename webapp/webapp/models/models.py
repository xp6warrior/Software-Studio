import reflex as rx
from sqlmodel import Field, Relationship
from sqlalchemy import Column, Enum
from typing import List, Optional
from . import enums as e

def enum_field(enum_cls, enum_name):
    return Field(
        sa_column = Column(Enum(enum_cls, name=enum_name, create_type=False), nullable=False)
    )


class PersonalItems(rx.Model, table=True):
    __table_args__ = {"schema": "Lost_Found"}

    id: int = Field(primary_key=True)
    type: e.PersonalItemType = enum_field(e.PersonalItemType, "PersonalItemType")
    color: e.ColorEnum = enum_field(e.ColorEnum, "ColorEnum")
    description: str
    status: e.StatusEnum = enum_field(e.StatusEnum, "StatusEnum")
    account_id: int = Field(foreign_key="account.id")

    account: Optional["Accounts"] = Relationship(
        back_populates="personal_items"
    )

class Jewelry(rx.Model, table=True):
    __table_args__ = {"schema": "Lost_Found"}

    id: int = Field(primary_key=True)
    type: e.JewelryType = enum_field(e.JewelryType, "JewelryType")
    color: e.ColorEnum = enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = enum_field(e.SizeEnum, "SizeEnum")
    description: str
    status: e.StatusEnum = enum_field(e.StatusEnum, "StatusEnum")
    account_id: int = Field(foreign_key="account.id")

    account: Optional["Accounts"] = Relationship(
        back_populates="jewelry"
    )

class Accessories(rx.Model, table=True):
    __table_args__ = {"schema": "Lost_Found"}

    id: int = Field(primary_key=True)
    type: e.AccessoryType = enum_field(e.AccessoryType, "AccessoryType")
    color: e.ColorEnum = enum_field(e.ColorEnum, "ColorEnum")
    material: e.MaterialEnum = enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    status: e.StatusEnum = enum_field(e.StatusEnum, "StatusEnum")
    account_id: int = Field(foreign_key="account.id")

    account: Optional["Accounts"] = Relationship(
        back_populates="accessories"
    )

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
    account_id: int = Field(foreign_key="account.id")

    account: Optional["Accounts"] = Relationship(
        back_populates="travel_items"
    )

class ElectronicDevices(rx.Model, table=True):
    __table_args__ = {"schema": "Lost_Found"}

    id: int = Field(primary_key=True)
    type: e.ElectronicDeviceType = enum_field(e.ElectronicDeviceType, "ElectronicDeviceType")
    color: e.ColorEnum = enum_field(e.ColorEnum, "ColorEnum")
    material: e.MaterialEnum = enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    status: e.StatusEnum = enum_field(e.StatusEnum, "StatusEnum")
    account_id: int = Field(foreign_key="account.id")

    account: Optional["Accounts"] = Relationship(
        back_populates="electronic_devices"
    )

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
    account_id: int = Field(foreign_key="account.id")

    account: Optional["Accounts"] = Relationship(
        back_populates="clothing"
    )

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
    account_id: int = Field(foreign_key="account.id")

    account: Optional["Accounts"] = Relationship(
        back_populates="office_items"
    )

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
    account_id: int = Field(foreign_key="account.id")

    account: Optional["Accounts"] = Relationship(
        back_populates="other_items"
    )

class Accounts(rx.Model, table=True):
    __table_args__ = {"schema": "Accounts"}

    id: int = Field(primary_key=True)
    email: str
    password: str
    role: e.RoleEnum = enum_field(e.RoleEnum, "RoleEnum")

    personal_items: List[PersonalItems] = Relationship(
        back_populates="account"
    )
    jewelry: List[Jewelry] = Relationship(
        back_populates="account"
    )
    accessories: List[Accessories] = Relationship(
        back_populates="account"
    )
    travel_items: List[TravelItems] = Relationship(
        back_populates="account"
    )
    electronic_devices: List[ElectronicDevices] = Relationship(
        back_populates="account"
    )
    clothing: List[Clothing] = Relationship(
        back_populates="account"
    )
    office_items: List[OfficeItems] = Relationship(
        back_populates="account"
    )
    other_items: List[OtherItems] = Relationship(
        back_populates="account"
    )