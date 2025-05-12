from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from .enums import *

Base = declarative_base()

class Accounts(Base):
    __tablename__ = 'accounts'
    __table_args__ = {'schema': 'accounts'}

    email = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    role = enum_field(RoleEnum, "RoleEnum")

class PersonalItems(Base):
    __tablename__ = 'personalitems'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = enum_field(PersonalItemType, "PersonalItemType")
    color = enum_field(ColorEnum, "ColorEnum")
    description = Column(String)
    status = enum_field(StatusEnum, "StatusEnum")
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class Jewelry(Base):
    __tablename__ = 'jewelry'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = enum_field(JewelryType, "JewelryType")
    color = enum_field(ColorEnum, "ColorEnum")
    size = enum_field(SizeEnum, "SizeEnum")
    description = Column(String)
    status = enum_field(StatusEnum, "StatusEnum")
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class Accessories(Base):
    __tablename__ = 'accessories'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = enum_field(AccessoryType, "AccessoryType")
    color = enum_field(ColorEnum, "ColorEnum")
    material = enum_field(MaterialEnum, "MaterialEnum")
    brand = Column(String)
    description = Column(String)
    status = enum_field(StatusEnum, "StatusEnum")
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class TravelItems(Base):
    __tablename__ = 'travelitems'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = enum_field(TravelItemType, "TravelItemType")
    color = enum_field(ColorEnum, "ColorEnum")
    size = enum_field(SizeEnum, "SizeEnum")
    material = enum_field(MaterialEnum, "MaterialEnum")
    brand = Column(String)
    description = Column(String)
    status = enum_field(StatusEnum, "StatusEnum")
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class ElectronicDevices(Base):
    __tablename__ = 'electronicdevices'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = enum_field(ElectronicDeviceType, "ElectronicDeviceType")
    color = enum_field(ColorEnum, "ColorEnum")
    material = enum_field(MaterialEnum, "MaterialEnum")
    brand = Column(String)
    description = Column(String)
    status = enum_field(StatusEnum, "StatusEnum")
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class Clothing(Base):
    __tablename__ = 'clothing'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = enum_field(ClothingType, "ClothingType")
    color = enum_field(ColorEnum, "ColorEnum")
    size = enum_field(SizeEnum, "SizeEnum")
    material = enum_field(MaterialEnum, "MaterialEnum")
    brand = Column(String)
    description = Column(String)
    status = enum_field(StatusEnum, "StatusEnum")
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class OfficeItems(Base):
    __tablename__ = 'officeitems'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = enum_field(OfficeItemType, "OfficeTypeItem")
    color = enum_field(ColorEnum, "ColorEnum")
    size = enum_field(SizeEnum, "SizeEnum")
    material = enum_field(MaterialEnum, "MaterialEnum")
    name = Column(String)
    description = Column(String)
    status = enum_field(StatusEnum, "StatusEnum")
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class OtherItems(Base):
    __tablename__ = 'otheritems'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = Column(String)  # free text
    color = enum_field(ColorEnum, "ColorEnum")
    size = enum_field(SizeEnum, "SizeEnum")
    material = enum_field(MaterialEnum, "MaterialEnum")
    brand = Column(String)
    name = Column(String)
    description = Column(String)
    status = enum_field(StatusEnum, "StatusEnum")
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class Match(Base):
    __tablename__ = 'match'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    table_name = Column(String, nullable=False)
    lost_item_id = Column(Integer, nullable=False)
    found_item_id = Column(Integer, nullable=False)
    status = enum_field(MatchStatus, "MatchStatus")
    percentage = Column(Integer, nullable=False)
