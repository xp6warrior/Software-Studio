import unittest
import reflex as rx
import webapp.models.enums as enums
from webapp.models.models import Accounts 
from webapp.backend.repository.login_repo import *

class TestSelectAndInsertAccount(unittest.TestCase):
    # Success
    def test_select_and_insert_account_success(self):
        account_obj = Accounts(
            email="abc@123.com",
            password="password",
            role=enums.RoleEnum.ADMIN
        )

        insert_account(account_obj)
        returned_obj = select_account("abc@123.com")
        self.assertEqual(returned_obj, account_obj)


if __name__ == "__main__":
    unittest.main()