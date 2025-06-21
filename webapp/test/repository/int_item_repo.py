import unittest
import reflex as rx
from sqlalchemy import delete

from webapp.models2.models import Items, Accounts, PersonalItems, Jewelry, Matches
from webapp.models2.enums import RoleEnum, StatusEnum, ColorEnum, SizeEnum, PersonalItemType, JewelryType, MatchStatusEnum
from webapp.repository.item_repo import *

class TestItemRepo(unittest.TestCase):

    def setUp(self):
        self.account = Accounts(email="test@domain.com", password="pass", role=RoleEnum.USER, 
                                 name="name", surname="surname")
        self.item1 = PersonalItems(status=StatusEnum.LOST, description="My item", email="test@domain.com",
                                   type=PersonalItemType.PASSPORT, color=ColorEnum.RED)
        self.item2 = Jewelry(status=StatusEnum.FOUND, description="My jewelry", email="test@domain.com",
                                   type=JewelryType.NECKLACE, color=ColorEnum.GREEN, size=SizeEnum.XS)
    
    def tearDown(self):
        with rx.session() as session:
            session.exec(delete(Accounts))
            session.exec(delete(Items))
            session.commit()

    # select_items_by_email
    def test_select_items_by_email_success(self):
        with rx.session() as session:
            session.add_all([self.account, self.item1, self.item2])
            session.commit()
            session.refresh(self.item1)
            session.refresh(self.item2)

        expected_results = [self.item1, self.item2]
        results = select_items_by_email("test@domain.com")
        self.assertCountEqual(expected_results, results)

    def test_select_items_by_email_success_email_no_exists(self):
        expected_results = []
        results = select_items_by_email("test@domain.com")
        self.assertCountEqual(expected_results, results)

    def test_select_items_by_email_fail_param(self):
        with self.assertRaises(Exception) as context:
            select_items_by_email(None)
        self.assertEqual(str(context.exception), "select_items_by_email parameter must not be None!")

        with self.assertRaises(Exception) as context:
            select_items_by_email(1234)
        self.assertEqual(str(context.exception), "select_items_by_email parameter must be of type str!")

    # select_item_by_id
    def test_select_item_buy_id_success(self):
        with rx.session() as session:
            session.add_all([self.account, self.item1, self.item2])
            session.commit()
            session.refresh(self.item1)
            session.refresh(self.item2)

        expected_results = self.item1
        results = select_item_by_id(self.item1.id)
        self.assertEqual(expected_results, results)

    # insert/update_item
    def test_insert_item_success(self):
        with rx.session() as session:
            session.add(self.account)
            session.commit()
            session.refresh(self.account)

        insert_update_item(self.item1)

        with rx.session() as session:
            result = session.exec(
                select(Items).where(Items.email == self.account.email)
            ).scalars().all()
            for r in result:
                session.refresh(r)

        expected_result = [self.item1]
        self.assertCountEqual(expected_result, result)
    
    def test_update_item_success(self):
        with rx.session() as session:
            session.add_all([self.account, self.item1])
            session.commit()
            session.refresh(self.account)
            session.refresh(self.item1)

        self.item1.description = "Test update."
        insert_update_item(self.item1)

        with rx.session() as session:
            result = session.exec(
                select(Items).where(Items.email == self.account.email)
            ).scalars().all()
            for r in result:
                session.refresh(r)

        expected_result = [self.item1]
        self.assertCountEqual(expected_result, result)

    def test_insert_update_item_fail_account_no_exists(self):
        with self.assertRaises(Exception):
            insert_update_item(self.item1)

    def test_insert_update_item_fail_param(self):
        with self.assertRaises(Exception) as context:
            insert_update_item(None)
        self.assertEqual(str(context.exception), "insert_update_item parameter must not be None!")

        with self.assertRaises(Exception) as context:
            insert_update_item(1234)
        self.assertEqual(str(context.exception), "insert_update_item parameter must be of type Items or ArchivedItems!")

    # delete_item
    def test_delete_item_success(self):
        with rx.session() as session:
            session.add_all([self.account, self.item1])
            session.commit()
            session.refresh(self.account)
            session.refresh(self.item1)

        delete_item(self.item1.id)

        with rx.session() as session:
            result = session.exec(
                select(Items).where(Items.id == self.item1.id)
            ).scalars().all()
            for r in result:
                session.refresh(r)

        expected_result = []
        self.assertCountEqual(expected_result, result)

    def test_delete_item_fail_item_no_exists(self):
        with self.assertRaises(Exception):
            delete_item(self.item1.id)

    def test_delete_item_fail_param(self):
        with self.assertRaises(Exception) as context:
            delete_item(None)
        self.assertEqual(str(context.exception), "delete_item parameter must not be None!")

        with self.assertRaises(Exception) as context:
            delete_item("test")
        self.assertEqual(str(context.exception), "delete_item parameter must be of type int!")

if __name__ == "__main__":
    unittest.main()