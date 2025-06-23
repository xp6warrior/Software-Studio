from sqlalchemy import Column, Integer, String, DateTime, PrimaryKeyConstraint, ForeignKeyConstraint, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.inspection import inspect

from .enums import *

"""
    !!! VERY IMPORTANT Sqlalchemy mechanisms !!!
    When creating an instance of once of these classes, it is in a 'transient' state.
    It is not in the database yet, you can freely assign and reference it's variables.
    
    Once you insert it into the DB via repo function (or had it returned from a select repo
    function), it is in a 'detached' state. This is because it has left an sqlalchemy
    session, which was within the function.
    
    You can still freely assign and reference it's variables. However, if you want
    to insert or update it to the DB again via repo function, YOU MUST NOT modify
    the corresponding row in the DB.

    Sqlalchemy assumes that the corresponding row in the DB remains untouched while the
    instance is detached. If you do not follow the conditions, in the case of insert,
    the row will not be inserted. In the case of an update, sqlalchemy will fail because
    it won't know which row to update. This will lead to errors.
"""

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
    password = Column(String(60), nullable=False)
    role = Column(postgresql.ENUM(RoleEnum), nullable=False)
    name = Column(String(20), nullable=False)
    surname = Column(String(30), nullable=False)
    last_login = Column(DateTime(), server_default=func.now(), nullable=False)
    last_submission = Column(DateTime())


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
    created_at = Column(DateTime(), server_default=func.now(), nullable=False)
    email = Column(String(254), nullable=False)

    _lost_matches = relationship("Matches", back_populates="lost_item", foreign_keys="Matches.lost_item_id", 
                                 lazy="write_only", passive_deletes=True)
    _found_matches = relationship("Matches", back_populates="found_item", foreign_keys="Matches.found_item_id", 
                                  lazy="write_only", passive_deletes=True)
    
    def to_dict(self):
        return {
            "id": str(self.id),
            "category": self.category.value,
            "status": self.status.value,
            "desc": self.description,
            "created_at": str(self.created_at),
            "email": self.email
        }
    
    def __str__(self):
        return f"Category: {self.category.value}, Description: {self.description}, Date submitted: {self.created_at}, "

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

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "it": self.type.value,
            "color": self.color.value
        })
        return base_dict
    
    def __str__(self):
        base_str = super().__str__()
        base_str += f"Type: {self.type.value}, Color: {self.color.value}"
        return base_str

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

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "it": self.type.value,
            "color": self.color.value,
            "size": self.size.value
        })
        return base_dict
    
    def __str__(self):
        base_str = super().__str__()
        base_str += f"Type: {self.type.value}, Color: {self.color.value}, Size: {self.size.value}"
        return base_str

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

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "it": self.type.value,
            "color": self.color.value,
            "material": self.material.value,
            "brand": self.brand
        })
        return base_dict
    
    def __str__(self):
        base_str = super().__str__()
        base_str += f"Type: {self.type.value}, Color: {self.color.value}, Material: {self.material.value}, Brand: {self.brand}"
        return base_str

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

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "it": self.type.value,
            "color": self.color.value,
            "size": self.size.value,
            "material": self.material.value,
            "brand": self.brand
        })
        return base_dict
    
    def __str__(self):
        base_str = super().__str__()
        base_str += f"Type: {self.type.value}, Color: {self.color.value}, Size: {self.size.value}, Material: {self.material.value}, Brand: {self.brand}"
        return base_str

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

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "it": self.type.value,
            "color": self.color.value,
            "material": self.material.value,
            "brand": self.brand
        })
        return base_dict
    
    def __str__(self):
        base_str = super().__str__()
        base_str += f"Type: {self.type.value}, Color: {self.color.value}, Material: {self.material.value}, Brand: {self.brand}"
        return base_str

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

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "it": self.type.value,
            "color": self.color.value,
            "size": self.size.value,
            "material": self.material.value,
            "brand": self.brand
        })
        return base_dict
    
    def __str__(self):
        base_str = super().__str__()
        base_str += f"Type: {self.type.value}, Color: {self.color.value}, Size: {self.size.value}, Material: {self.material.value}, Brand: {self.brand}"
        return base_str

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

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "it": self.type.value,
            "color": self.color.value,
            "size": self.size.value,
            "material": self.material.value,
            "name": self.name
        })
        return base_dict
    
    def __str__(self):
        base_str = super().__str__()
        base_str += f"Type: {self.type.value}, Color: {self.color.value}, Size: {self.size.value}, Material: {self.material.value}, Name: {self.name}"
        return base_str

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

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict.update({
            "it": self.type.value,
            "color": self.color.value,
            "size": self.size.value,
            "material": self.material.value,
            "brand": self.brand,
            "name": self.name
        })
        return base_dict
    
    def __str__(self):
        base_str = super().__str__()
        base_str += f"Type: {self.type.value}, Color: {self.color.value}, Size: {self.size.value}, Material: {self.material.value}, Brand: {self.brand}, Name: {self.name}"
        return base_str


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

    lost_item = relationship("Items", back_populates="_lost_matches", foreign_keys=[lost_item_id],
                             lazy="joined")
    found_item = relationship("Items", back_populates="_found_matches", foreign_keys=[found_item_id],
                              lazy="joined")
    
    # # TODO Figure out synopsis function
    # def __str__(self):
    #     synopsis = ""
    #     for k, v in self.found_item.to_dict().items():
    #         synopsis += f"{v} "
    #     synopsis += self.found_item.type
    #     return synopsis

class ArchivedItems(Base):
    __tablename__ = "archiveditems"
    __table_args__ = (
        PrimaryKeyConstraint("id", name="pk_archiveditems"),
        CheckConstraint("owner_pesel ~ '^[0-9]{11}$'", name="ck_archiveitems_pesel"),
        {"schema": "archive"}
    )

    id = Column(Integer)
    match_id = Column(Integer, nullable=False)
    item_summary = Column(String(255), nullable=False)
    owner_email = Column(String(254), nullable=False)
    owner_pesel = Column(String(11), nullable=False)
    owner_name = Column(String(20), nullable=False)
    owner_surname = Column(String(30), nullable=False)
    pickup_time = Column(DateTime(), server_default=func.now(), nullable=False)
