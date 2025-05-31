from sqlalchemy import Column, Integer, String, DateTime, PrimaryKeyConstraint, ForeignKeyConstraint, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.inspection import inspect

from .enums import *

class Base(DeclarativeBase):
    def __eq__(self, other):
        if type(self) != type(other):
            return False

        # Get all column keys
        self_columns = inspect(self).mapper.column_attrs
        for col in self_columns:
            if getattr(self, col.key) != getattr(other, col.key):
                return False
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash(tuple(getattr(self, col.key) for col in inspect(self).mapper.column_attrs))
    
    def __repr__(self):
        values = ', '.join(
            f"{col.key}={getattr(self, col.key)!r}"
            for col in inspect(self).mapper.column_attrs
        )
        return f"<{self.__class__.__name__}({values})>"

class Accounts(Base):
    __tablename__ = "accounts"
    __table_args__ = (
        PrimaryKeyConstraint("email", name="pk_accounts"),
        {"schema": "accounts"}
    )

    email = Column(String(254))
    password = Column(String(30), nullable=False)
    role = Column(postgresql.ENUM(RoleEnum), nullable=False)
    name = Column(String(20), nullable=False)
    surname = Column(String(30), nullable=False)
    last_login = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Items(Base):
    __tablename__ = "items"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_items"),
        ForeignKeyConstraint(["email"], ["accounts.accounts.email"], name="pk_items_email"),
        {"schema": "lost_found"}
    )

    id = Column(Integer)
    status = Column(postgresql.ENUM(StatusEnum), nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    email = Column(String(254), nullable=False)

class PersonalItems(Base):
    __tablename__ = "personalitems"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_personalitems"),
        ForeignKeyConstraint(["item"], ["lost_found.items.id"], name="pk_personalitems_item"),
        UniqueConstraint("item", name="uq_personalitems_item"),
        {"schema": "lost_found"}
    )

    id = Column(Integer)
    type = Column(postgresql.ENUM(PersonalItemType), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    item = Column(Integer, nullable=False)

class Jewelry(Base):
    __tablename__ = "jewelry"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_jewelry"),
        ForeignKeyConstraint(["item"], ["lost_found.items.id"], name="pk_jewelry_item"),
        UniqueConstraint("item", name="uq_jewelry_item"),
        {"schema": "lost_found"}
    )

    id = Column(Integer)
    type = Column(postgresql.ENUM(JewelryType), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    size = Column(postgresql.ENUM(SizeEnum), nullable=False)
    item = Column(Integer, nullable=False)

class Accessories(Base):
    __tablename__ = "accessories"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_accessories"),
        ForeignKeyConstraint(["item"], ["lost_found.items.id"], name="pk_accessories_item"),
        UniqueConstraint("item", name="uq_accessories_item"),
        {"schema": "lost_found"}
    )

    id = Column(Integer)
    type = Column(postgresql.ENUM(AccessoryType), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    material = Column(postgresql.ENUM(MaterialEnum), nullable=False)
    brand = Column(String(20), nullable=False)
    item = Column(Integer, nullable=False)

class TravelItems(Base):
    __tablename__ = "travelitems"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_travelitems"),
        ForeignKeyConstraint(["item"], ["lost_found.items.id"], name="fk_travelitems_item"),
        UniqueConstraint("item", name="uq_travelitems_item"),
        {"schema": "lost_found"}
    )

    id = Column(Integer)
    type = Column(postgresql.ENUM(TravelItemType), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    size = Column(postgresql.ENUM(SizeEnum), nullable=False)
    material = Column(postgresql.ENUM(MaterialEnum), nullable=False)
    brand = Column(String(20), nullable=False)
    item = Column(Integer, nullable=False)

class ElectronicDevices(Base):
    __tablename__ = "electronicdevices"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_electronicdevices"),
        ForeignKeyConstraint(["item"], ["lost_found.items.id"], name="fk_electronicdevices_item"),
        UniqueConstraint("item", name="uq_electronicdevices_item"),
        {"schema": "lost_found"}
    )

    id = Column(Integer)
    type = Column(postgresql.ENUM(ElectronicDeviceType), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    material = Column(postgresql.ENUM(MaterialEnum), nullable=False)
    brand = Column(String(20), nullable=False)
    item = Column(Integer, nullable=False)

class Clothing(Base):
    __tablename__ = "clothing"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_clothing"),
        ForeignKeyConstraint(["item"], ["lost_found.items.id"], name="fk_clothing_item"),
        UniqueConstraint("item", name="uq_clothing_item"),
        {"schema": "lost_found"}
    )

    id = Column(Integer)
    type = Column(postgresql.ENUM(ClothingType), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    size = Column(postgresql.ENUM(SizeEnum), nullable=False)
    material = Column(postgresql.ENUM(MaterialEnum), nullable=False)
    brand = Column(String(20), nullable=False)
    item = Column(Integer, nullable=False)

class OfficeItems(Base):
    __tablename__ = "officeitems"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_officeitems"),
        ForeignKeyConstraint(["item"], ["lost_found.items.id"], name="fk_officeitems_item"),
        UniqueConstraint("item", name="uq_officeitems_item"),
        {"schema": "lost_found"}
    )

    id = Column(Integer)
    type = Column(postgresql.ENUM(OfficeItemType), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    size = Column(postgresql.ENUM(SizeEnum), nullable=False)
    material = Column(postgresql.ENUM(MaterialEnum), nullable=False)
    name = Column(String(20), nullable=False)
    item = Column(Integer, nullable=False)

class OtherItems(Base):
    __tablename__ = "otheritems"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_otheritems"),
        ForeignKeyConstraint(["item"], ["lost_found.items.id"], name="fk_otheritems_item"),
        UniqueConstraint("item", name="uq_item"),
        {"schema": "lost_found"}
    )

    id = Column(Integer)
    type = Column(String(20), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    size = Column(postgresql.ENUM(SizeEnum), nullable=False)
    material = Column(postgresql.ENUM(MaterialEnum), nullable=False)
    brand = Column(String(20), nullable=False)
    name = Column(String(20), nullable=False)
    item = Column(Integer, nullable=False)


class Matches(Base):
    __tablename__ = "matches"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_matches"),
        CheckConstraint("percentage <= 100 AND percentage > 0", name="ck_matches_percentage"),
        ForeignKeyConstraint(["lost_item_id"], ["lost_found.items.id"], name="fk_matches_lost_item"),
        ForeignKeyConstraint(["found_item_id"], ["lost_found.items.id"], name="fk_matches_found_item"),
        {"schema": "matches"}
    )

    id = Column(Integer)
    status = Column(postgresql.ENUM(MatchStatusEnum), nullable=False)
    percentage = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    lost_item_id = Column(Integer, nullable=False)
    found_item_id = Column(Integer, nullable=False)


class ArchivedItems(Base):
    __tablename__ = "archiveditems"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_archiveditems"),
        {"schema": "archive"}
    )

    id = Column(Integer)
    item_summary = Column(String(255), nullable=False)
    owner_email = Column(String(254), nullable=False)
    owner_pesel = Column(Integer, nullable=False)
    owner_name = Column(String(20), nullable=False)
    owner_surname = Column(String(30), nullable=False)
    pickup_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
