import unittest
import reflex
from webapp.models.enums import RoleEnum
from webapp.models.models import Accounts 
from webapp.repository.account_repo import *

class TestAccountRepo(unittest.TestCase):

    def setUp(self):
        self.account1 = Accounts(
            email="abc@123.com",
            password="password",
            role=RoleEnum.ADMIN
        )
        self.account2 = Accounts(
            email="def@456.com",
            password="password",
            role=RoleEnum.WORKER
        )

    def test_account_crud(self):
        # Insert and select
        insert_update_account(self.account1)
        selected = select_account(self.account1.email)
        self.assertEqual(selected, self.account1)
        insert_update_account(self.account2)
        selected = select_account(self.account2.email)
        self.assertEqual(selected, self.account2)

        # Insert exceptions
        with self.assertRaises(Exception) as context:
            insert_update_account(None)
        self.assertEqual(str(context.exception), "insert_update_account parameter must not be None!")
        with self.assertRaises(Exception) as context:
            insert_update_account(5)
        self.assertEqual(str(context.exception), "insert_update_account parameter must be of type Accounts!")

        # Select exceptions
        with self.assertRaises(Exception) as context:
            select_account(None)
        self.assertEqual(str(context.exception), "select_account parameter must not be None!")
        with self.assertRaises(Exception) as context:
            select_account(5)
        self.assertEqual(str(context.exception), "select_account parameter must be of type str!")

        selected = select_account("other@other.com")
        self.assertEqual(selected, None)

        # Select all accounts
        selected = select_all_accounts()
        self.assertCountEqual(selected, [self.account1, self.account2])

        # Update and select
        self.account2.role = RoleEnum.USER
        insert_update_account(self.account2)
        selected = select_account(self.account2.email)
        self.assertEqual(selected, self.account2)

        # Delete and select
        delete_account(self.account1)
        delete_account(self.account2)
        selected = select_all_accounts()
        self.assertEqual(selected, [])

        # Delete exceptions
        with self.assertRaises(Exception) as context:
            delete_account(None)
        self.assertEqual(str(context.exception), "delete_account parameter must not be None!")
        with self.assertRaises(Exception) as context:
            delete_account(5)
        self.assertEqual(str(context.exception), "delete_account parameter must be of type Accounts!")


if __name__ == "__main__":
    unittest.main()