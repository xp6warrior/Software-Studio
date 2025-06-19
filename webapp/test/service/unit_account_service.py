import unittest
import string
from unittest.mock import patch, call
from webapp.models2.enums import RoleEnum
from webapp.models2.models import Accounts

from webapp.service.account_service import *

class TestCreateAccount(unittest.TestCase):

    def setUp(self):
        self.account = Accounts(
            email="test@domain.com",
            password="password",
            role = RoleEnum.USER,
            name = "name",
            surname = "surname"
        )

    @patch("webapp.service.account_service.insert_update_account")
    def test_create_account_success(self, mock_insert_update_account):
        create_account(self.account.email, self.account.password, self.account.role, self.account.name, self.account.surname)
        mock_insert_update_account.assert_called_once_with(self.account)

    @patch("webapp.service.account_service.insert_update_account")
    def test_create_account_success_no_pass(self, mock_insert_update_account):
        create_account(self.account.email, None, self.account.role, self.account.name, self.account.surname)
        mock_insert_update_account.assert_called()
        
        args, kwargs = mock_insert_update_account.call_args
        password = args[0].password

        self.assertTrue(len(password) == 14)
        self.assertTrue(
            any(c in string.ascii_letters for c in password) or
            any(c in string.digits for c in password) or
            any(c in string.punctuation for c in password)
        )

    def test_create_account_fail_invalid_email(self):
        result = create_account("not_valid_email", self.account.password, self.account.role, self.account.name, self.account.surname)
        self.assertEqual(result, "Error: Invalid email address!")

    @patch("webapp.service.account_service.select_account_by_email")
    def test_login_success(self, mock_select_account_by_email):
        mock_select_account_by_email.return_value = self.account
        result = login(self.account.email, self.account.password)

        mock_select_account_by_email.assert_called_once_with(self.account.email)
        self.assertEqual(result, "user")

    @patch("webapp.service.account_service.select_account_by_email")
    def test_login_fail(self, mock_select_account_by_email):
        mock_select_account_by_email.return_value = None
        result = login(self.account.email, self.account.password)
        self.assertFalse(result)

        mock_select_account_by_email.return_value = self.account
        result = login(self.account.email, "other_password")
        self.assertFalse(result)

        mock_select_account_by_email.assert_has_calls([call(self.account.email), call(self.account.email)])

    @patch("webapp.service.account_service.select_account_by_email")
    def test_get_user_account_details_success(self, mock_select_account_by_email):
        mock_select_account_by_email.return_value = self.account
        result = get_user_account_details(self.account.email)

        mock_select_account_by_email.assert_called_once_with(self.account.email)
        self.assertEqual(result, {
            "name": self.account.name,
            "surname": self.account.surname,
            "email": self.account.email,
            "role": self.account.role
        })

    @patch("webapp.service.account_service.select_account_by_email")
    def test_get_user_account_details_fail(self, mock_select_account_by_email):
        mock_select_account_by_email.return_value = None
        result = get_user_account_details(self.account.email)

        mock_select_account_by_email.assert_called_once_with(self.account.email)
        self.assertFalse(result)

    @patch("webapp.service.account_service.select_all_accounts")
    def test_get_accounts_success(self, mock_select_all_accounts):
        mock_select_all_accounts.return_value = [self.account]
        result = get_accounts()

        mock_select_all_accounts.assert_called_once()
        self.assertEqual(result, [{
            "name": self.account.name,
            "surname": self.account.surname,
            "email": self.account.email,
            "role": self.account.role
        }])

    @patch("webapp.service.account_service.select_account_by_email")
    def test_delete_account_fail(self, mock_select_account_by_email):
        mock_select_account_by_email.return_value = None
        result = delete_account("other@email.com")

        mock_select_account_by_email.assert_called_once_with("other@email.com")
        self.assertFalse(result)

    @patch("webapp.service.account_service.delete_account_from_repo")
    @patch("webapp.service.account_service.select_account_by_email")
    def test_delete_account_success(self, mock_select_account_by_email, mock_delete_account):
        mock_select_account_by_email.return_value = self.account
        result = delete_account(self.account.email)

        mock_select_account_by_email.assert_called_once_with(self.account.email)
        mock_delete_account.assert_called_once_with(self.account)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()