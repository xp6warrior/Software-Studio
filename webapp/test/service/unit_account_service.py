import unittest
from unittest.mock import patch, call
from webapp.models.enums import RoleEnum
from webapp.models.models import Accounts

from webapp.service.account_service import *

class TestCreateAccount(unittest.TestCase):

    @patch("webapp.service.account_service.insert_update_account")
    def test_create_account_success(self, mock_insert_update_account):
        email = "test@domain.com"
        password = "password"
        role = RoleEnum.USER
        pesel = 12345
        name = "name"
        surname = "surname"
        account = Accounts(email=email, password=password, role=role, pesel=pesel, name=name, surname=surname)

        result = create_account(email, password, role, pesel, name, surname)
        mock_insert_update_account.assert_called_once_with(account)
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()