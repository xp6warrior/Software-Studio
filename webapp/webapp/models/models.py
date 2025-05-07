import reflex as rx
from sqlmodel import Field
from . import enums as e

class Accounts(rx.Model, table=True):
    __table_args__ = {"schema": "accounts"}

    id: int = Field(primary_key=True)
    email: str
    password: str
    role: e.RoleEnum = e.enum_field(e.RoleEnum, "RoleEnum")


class PersonalItems(rx.Model, table=True):
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: e.PersonalItemType = e.enum_field(e.PersonalItemType, "PersonalItemType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")
    account_id: int = Field(foreign_key="accounts.accounts.id")


class Jewelry(rx.Model, table=True):
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: e.JewelryType = e.enum_field(e.JewelryType, "JewelryType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = e.enum_field(e.SizeEnum, "SizeEnum")
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")

    account_id: int = Field(foreign_key="accounts.accounts.id")

class Accessories(rx.Model, table=True):
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: e.AccessoryType = e.enum_field(e.AccessoryType, "AccessoryType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")

    account_id: int = Field(foreign_key="accounts.accounts.id")


class TravelItems(rx.Model, table=True):
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: e.TravelItemType = e.enum_field(e.TravelItemType, "TravelItemType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = e.enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")

    account_id: int = Field(foreign_key="accounts.accounts.id")


class ElectronicDevices(rx.Model, table=True):
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: e.ElectronicDeviceType = e.enum_field(e.ElectronicDeviceType, "ElectronicDeviceType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")

    account_id: int = Field(foreign_key="accounts.accounts.id")

class Clothing(rx.Model, table=True):
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: e.ClothingType = e.enum_field(e.ClothingType, "ClothingType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = e.enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    brand: str
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")

    account_id: int = Field(foreign_key="accounts.accounts.id")

class OfficeItems(rx.Model, table=True):
    __table_args__ = {"schema": "lost_found"}

    id: int = Field(primary_key=True)
    type: e.OfficeItemType = e.enum_field(e.OfficeItemType, "OfficeItemType")
    color: e.ColorEnum = e.enum_field(e.ColorEnum, "ColorEnum")
    size: e.SizeEnum = e.enum_field(e.SizeEnum, "SizeEnum")
    material: e.MaterialEnum = e.enum_field(e.MaterialEnum, "MaterialEnum")
    name: str
    description: str
    status: e.StatusEnum = e.enum_field(e.StatusEnum, "StatusEnum")

    account_id: int = Field(foreign_key="accounts.accounts.id")

class OtherItems(rx.Model, table=True):
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

    account_id: int = Field(foreign_key="accounts.accounts.id")