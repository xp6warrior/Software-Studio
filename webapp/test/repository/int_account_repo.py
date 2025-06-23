import unittest
import reflex as rx
from sqlalchemy import delete

from webapp.models2.models import Accounts 
from webapp.models2.enums import RoleEnum
from webapp.repository.account_repo import *

class TestAccountRepo(unittest.TestCase):

    def setUp(self):
        self.account1 = Accounts(email="test@domain.com", password="pass", role=RoleEnum.USER,
                        name="name", surname="surname")
        self.account2 = Accounts(email="test2@domain.com", password="pass2", role=RoleEnum.WORKER,
                        name="name2", surname="surname2")
        self.account3 = Accounts(email="test@domain.com", password="pass3", role=RoleEnum.ADMIN,
                        name="name3", surname="surname3")

    def tearDown(self):
        with rx.session() as session:
            session.exec(delete(Accounts))
            session.commit()

    # select_account_by_email
    def test_select_account_by_email_success_none(self):
        result = select_account_by_email("test@domain.com")
        self.assertIsNone(result)

    def test_select_account_by_email_success_one(self):
        with rx.session() as session:
            session.add(self.account1)
            session.commit()
            session.refresh(self.account1)
        
        expected_result = self.account1
        result = select_account_by_email("test@domain.com")
        self.assertEqual(expected_result, result)

    def test_select_account_by_email_fail_param(self):
        with self.assertRaises(Exception) as context:
            select_account_by_email(None)
        self.assertEqual(str(context.exception), "select_account_by_email parameter must not be None!")

        with self.assertRaises(Exception) as context:
            select_account_by_email(1234)
        self.assertEqual(str(context.exception), "select_account_by_email parameter must be of type str!")
        
    # select_all_accounts
    def test_select_all_accounts_success_none(self):
        result = select_all_accounts()
        self.assertEqual([], result)

    def test_select_all_accounts_success_many(self):
        with rx.session() as session:
            session.add_all([self.account1, self.account2])
            session.commit()
            session.refresh(self.account1)
            session.refresh(self.account2)

        expected_result = [self.account1, self.account2]
        result = select_all_accounts()
        self.assertCountEqual(expected_result, result)
    
    # insert/update account
    def test_insert_account_success(self):
        insert_update_account(self.account1)

        with rx.session() as session:
            result = session.exec(
                select(Accounts).where(Accounts.email == self.account1.email)
            ).scalars().first()

        expected_result = self.account1
        self.assertEqual(expected_result, result)

    def test_update_account_success(self):
        with rx.session() as session:
            session.add(self.account1)
            session.commit()
            session.refresh(self.account1)

        self.account1.role = RoleEnum.ADMIN
        insert_update_account(self.account1)

        with rx.session() as session:
            result = session.exec(
                select(Accounts).where(Accounts.email == self.account1.email)
            ).scalars().first()

        expected_result = self.account1
        self.assertEqual(expected_result, result)

    def test_insert_account_fail_exists(self):
        insert_update_account(self.account1)
        with self.assertRaises(Exception):
            insert_update_account(self.account3)

    def test_insert_account_fail_param(self):
        with self.assertRaises(Exception) as context:
            insert_update_account(None)
        self.assertEqual(str(context.exception), "insert_update_account parameter must not be None!")

        with self.assertRaises(Exception) as context:
            insert_update_account(1234)
        self.assertEqual(str(context.exception), "insert_update_account parameter must be of type Accounts!")

    # delete_account
    def test_delete_account_success(self):
        with rx.session() as session:
            session.add(self.account1)
            session.commit()
            session.refresh(self.account1)

        delete_account(self.account1)

        with rx.session() as session:
            result = session.exec(
                select(Accounts).where(Accounts.email == self.account1.email)
            ).scalars().first()

        self.assertIsNone(result)

    def test_delete_account_fail_param(self):
        with self.assertRaises(Exception) as context:
            delete_account(None)
        self.assertEqual(str(context.exception), "delete_account parameter must not be None!")

        with self.assertRaises(Exception) as context:
            delete_account(1234)
        self.assertEqual(str(context.exception), "delete_account parameter must be of type Accounts!")

    def test_delete_account_fail_no_exists(self):
        with self.assertRaises(Exception):
            delete_account(self.account1)

if __name__ == "__main__":
    unittest.main()