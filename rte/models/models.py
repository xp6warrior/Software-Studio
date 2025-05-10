from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from .enums import *

Base = declarative_base()

class Accounts(Base):
    __tablename__ = 'accounts'
    __table_args__ = {'schema': 'accounts'}

    email = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)

class PersonalItems(Base):
    __tablename__ = 'personalitems'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = Column(Enum(PersonalItemType), nullable=False)
    color = Column(Enum(ColorEnum), nullable=False)
    description = Column(String)
    status = Column(Enum(StatusEnum), nullable=False)
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class Jewelry(Base):
    __tablename__ = 'jewelry'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = Column(Enum(JewelryType), nullable=False)
    color = Column(Enum(ColorEnum), nullable=False)
    size = Column(Enum(SizeEnum), nullable=False)
    description = Column(String)
    status = Column(Enum(StatusEnum), nullable=False)
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class Accessories(Base):
    __tablename__ = 'accessories'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = Column(Enum(AccessoryType), nullable=False)
    color = Column(Enum(ColorEnum), nullable=False)
    material = Column(Enum(MaterialEnum), nullable=False)
    brand = Column(String)
    description = Column(String)
    status = Column(Enum(StatusEnum), nullable=False)
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class TravelItems(Base):
    __tablename__ = 'travelitems'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = Column(Enum(TravelItemType), nullable=False)
    color = Column(Enum(ColorEnum), nullable=False)
    size = Column(Enum(SizeEnum), nullable=False)
    material = Column(Enum(MaterialEnum), nullable=False)
    brand = Column(String)
    description = Column(String)
    status = Column(Enum(StatusEnum), nullable=False)
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class ElectronicDevices(Base):
    __tablename__ = 'electronicdevices'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = Column(Enum(ElectronicDeviceType), nullable=False)
    color = Column(Enum(ColorEnum), nullable=False)
    material = Column(Enum(MaterialEnum), nullable=False)
    brand = Column(String)
    description = Column(String)
    status = Column(Enum(StatusEnum), nullable=False)
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class Clothing(Base):
    __tablename__ = 'clothing'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = Column(Enum(ClothingType), nullable=False)
    color = Column(Enum(ColorEnum), nullable=False)
    size = Column(Enum(SizeEnum), nullable=False)
    material = Column(Enum(MaterialEnum), nullable=False)
    brand = Column(String)
    description = Column(String)
    status = Column(Enum(StatusEnum), nullable=False)
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class OfficeItems(Base):
    __tablename__ = 'officeitems'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = Column(Enum(OfficeItemType), nullable=False)
    color = Column(Enum(ColorEnum), nullable=False)
    size = Column(Enum(SizeEnum), nullable=False)
    material = Column(Enum(MaterialEnum), nullable=False)
    name = Column(String)
    description = Column(String)
    status = Column(Enum(StatusEnum), nullable=False)
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class OtherItems(Base):
    __tablename__ = 'otheritems'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    type = Column(String)  # free text
    color = Column(Enum(ColorEnum), nullable=False)
    size = Column(Enum(SizeEnum), nullable=False)
    material = Column(Enum(MaterialEnum), nullable=False)
    brand = Column(String)
    name = Column(String)
    description = Column(String)
    status = Column(Enum(StatusEnum), nullable=False)
    email = Column(String, ForeignKey('accounts.accounts.email'), nullable=False)

class Match(Base):
    __tablename__ = 'match'
    __table_args__ = {'schema': 'lost_found'}

    id = Column(Integer, primary_key=True)
    table_name = Column(String, nullable=False)
    lost_item_id = Column(Integer, nullable=False)
    found_item_id = Column(Integer, nullable=False)
    status = Column(Enum(MatchStatus), nullable=False)
