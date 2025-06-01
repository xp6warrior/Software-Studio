from sqlalchemy import Column, Integer, String, DateTime, PrimaryKeyConstraint, ForeignKeyConstraint, CheckConstraint
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
        ForeignKeyConstraint(["email"], ["accounts.accounts.email"], "fk_items_email", ondelete="CASCADE"),
        {"schema": "lost_found"}
    )
    __mapper_args__ = {"polymorphic_on": "category"}

    id = Column(Integer)
    category = Column(postgresql.ENUM(CategoryEnum), nullable=False)
    status = Column(postgresql.ENUM(StatusEnum), nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    email = Column(String(254), nullable=False)

class PersonalItems(Items):
    __tablename__ = "personalitems"
    __table_args__ = (
        PrimaryKeyConstraint("item_id", name="pk_personalitems"),
        ForeignKeyConstraint(["item_id"], ["lost_found.items.id"], "fk_personalitems_item_id", ondelete="CASCADE"),
        {"schema": "lost_found"}
    )
    __mapper_args__ = {"polymorphic_identity": CategoryEnum.PERSONAL_ITEMS}

    item_id = Column(Integer, nullable=False)
    type = Column(postgresql.ENUM(PersonalItemType), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)

class Jewelry(Items):
    __tablename__ = "jewelry"
    __table_args__ = (
        PrimaryKeyConstraint("item_id", name="pk_jewelry"),
        ForeignKeyConstraint(["item_id"], ["lost_found.items.id"], "fk_jewelry_item_id", ondelete="CASCADE"),
        {"schema": "lost_found"}
    )
    __mapper_args__ = {"polymorphic_identity": CategoryEnum.JEWELRY}

    item_id = Column(Integer, nullable=False)
    type = Column(postgresql.ENUM(JewelryType), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    size = Column(postgresql.ENUM(SizeEnum), nullable=False)

class Accessories(Items):
    __tablename__ = "accessories"
    __table_args__ = (
        PrimaryKeyConstraint("item_id", name="pk_accessories"),
        ForeignKeyConstraint(["item_id"], ["lost_found.items.id"], "fk_accessories_item_id", ondelete="CASCADE"),
        {"schema": "lost_found"}
    )
    __mapper_args__ = {"polymorphic_identity": CategoryEnum.ACCESSORIES}

    item_id = Column(Integer, nullable=False)
    type = Column(postgresql.ENUM(AccessoryType), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    material = Column(postgresql.ENUM(MaterialEnum), nullable=False)
    brand = Column(String(20), nullable=False)

class TravelItems(Items):
    __tablename__ = "travelitems"
    __table_args__ = (
        PrimaryKeyConstraint("item_id", name="pk_travelitems"),
        ForeignKeyConstraint(["item_id"], ["lost_found.items.id"], "fk_travelitems_item_id", ondelete="CASCADE"),
        {"schema": "lost_found"}
    )
    __mapper_args__ = {"polymorphic_identity": CategoryEnum.TRAVEL_ITEMS}

    item_id = Column(Integer, nullable=False)
    type = Column(postgresql.ENUM(TravelItemType), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    size = Column(postgresql.ENUM(SizeEnum), nullable=False)
    material = Column(postgresql.ENUM(MaterialEnum), nullable=False)
    brand = Column(String(20), nullable=False)

class ElectronicDevices(Items):
    __tablename__ = "electronicdevices"
    __table_args__ = (
        PrimaryKeyConstraint("item_id", name="pk_electronicdevices"),
        ForeignKeyConstraint(["item_id"], ["lost_found.items.id"], "fk_electronicdevices_item_id", ondelete="CASCADE"),
        {"schema": "lost_found"}
    )
    __mapper_args__ = {"polymorphic_identity": CategoryEnum.ELECTRONIC_DEVICES}

    item_id = Column(Integer, nullable=False)
    type = Column(postgresql.ENUM(ElectronicDeviceType), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    material = Column(postgresql.ENUM(MaterialEnum), nullable=False)
    brand = Column(String(20), nullable=False)

class Clothing(Items):
    __tablename__ = "clothing"
    __table_args__ = (
        PrimaryKeyConstraint("item_id", name="pk_clothing"),
        ForeignKeyConstraint(["item_id"], ["lost_found.items.id"], "fk_clothing_item_id", ondelete="CASCADE"),
        {"schema": "lost_found"}
    )
    __mapper_args__ = {"polymorphic_identity": CategoryEnum.CLOTHING}

    item_id = Column(Integer, nullable=False)
    type = Column(postgresql.ENUM(ClothingType), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    size = Column(postgresql.ENUM(SizeEnum), nullable=False)
    material = Column(postgresql.ENUM(MaterialEnum), nullable=False)
    brand = Column(String(20), nullable=False)

class OfficeItems(Items):
    __tablename__ = "officeitems"
    __table_args__ = (
        PrimaryKeyConstraint("item_id", name="pk_officeitems"),
        ForeignKeyConstraint(["item_id"], ["lost_found.items.id"], "fk_officeitems_item_id", ondelete="CASCADE"),
        {"schema": "lost_found"}
    )
    __mapper_args__ = {"polymorphic_identity": CategoryEnum.OFFICE_ITEMS}

    item_id = Column(Integer, nullable=False)
    type = Column(postgresql.ENUM(OfficeItemType), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    size = Column(postgresql.ENUM(SizeEnum), nullable=False)
    material = Column(postgresql.ENUM(MaterialEnum), nullable=False)
    name = Column(String(20), nullable=False)

class OtherItems(Items):
    __tablename__ = "otheritems"
    __table_args__ = (
        PrimaryKeyConstraint("item_id", name="pk_otheritems"),
        ForeignKeyConstraint(["item_id"], ["lost_found.items.id"], "fk_otheritems_item_id", ondelete="CASCADE"),
        {"schema": "lost_found"}
    )
    __mapper_args__ = {"polymorphic_identity": CategoryEnum.OTHER_ITEMS}

    item_id = Column(Integer, nullable=False)
    type = Column(String(20), nullable=False)
    color = Column(postgresql.ENUM(ColorEnum), nullable=False)
    size = Column(postgresql.ENUM(SizeEnum), nullable=False)
    material = Column(postgresql.ENUM(MaterialEnum), nullable=False)
    brand = Column(String(20), nullable=False)
    name = Column(String(20), nullable=False)


class Matches(Base):
    __tablename__ = "matches"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_matches"),
        CheckConstraint("percentage <= 100 AND percentage > 0", name="ck_matches_percentage"),
        ForeignKeyConstraint(["lost_item_id"], ["lost_found.items.id"], "fk_matches_lost_item", ondelete="CASCADE"),
        ForeignKeyConstraint(["found_item_id"], ["lost_found.items.id"], "fk_matches_found_item", ondelete="CASCADE"),
        {"schema": "matches"}
    )

    id = Column(Integer)
    status = Column(postgresql.ENUM(MatchStatusEnum), nullable=False)
    percentage = Column(Integer, nullable=False)
    status_changed = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    lost_item_id = Column(Integer, nullable=False)
    found_item_id = Column(Integer, nullable=False)


class ArchivedItems(Base):
    __tablename__ = "archiveditems"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_archiveditems"),
        CheckConstraint("owner_pesel ~ '^[0-9]{11}$'", name="ck_archiveitems_pesel"),
        {"schema": "archive"}
    )

    id = Column(Integer)
    item_summary = Column(String(255), nullable=False)
    owner_email = Column(String(254), nullable=False)
    owner_pesel = Column(String(11), nullable=False)
    owner_name = Column(String(20), nullable=False)
    owner_surname = Column(String(30), nullable=False)
    pickup_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
