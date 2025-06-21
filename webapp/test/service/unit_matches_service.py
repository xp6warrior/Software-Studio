import unittest
from unittest.mock import patch
from webapp.service.matches_service import *
from webapp.models2.models import PersonalItems, Matches, ArchivedItems
from webapp.models2.enums import CategoryEnum, StatusEnum, PersonalItemType, ColorEnum, MatchStatusEnum

class TestMatchesService(unittest.TestCase):

    def setUp(self):
        self.found_item = PersonalItems(
            id=1, category=CategoryEnum.PERSONAL_ITEMS, status=StatusEnum.FOUND,
            description="Personal Item", email="found@domain.com", type=PersonalItemType.PASSPORT, color=ColorEnum.RED
        )
        self.lost_item = PersonalItems(
            id=2, category=CategoryEnum.PERSONAL_ITEMS, status=StatusEnum.LOST,
            description="Personal Item", email="owner@domain.com", type=PersonalItemType.PASSPORT, color=ColorEnum.RED
        )
        self.unconfirmed_match = Matches(
            id=1, status=MatchStatusEnum.UNCONFIRMED, percentage=100, lost_item_id=2, found_item_id=1,
            lost_item=self.lost_item, found_item=self.found_item
        )
        self.confirmed_match = Matches(
            id=2, status=MatchStatusEnum.CONFIRMED, percentage=100, lost_item_id=2, found_item_id=1,
            lost_item=self.lost_item, found_item=self.found_item
        )
        self.archive_item = ArchivedItems(
            owner_email="owner@domain.com", owner_name="name", owner_surname="surname",
            owner_pesel="12345678910", item_summary="Category: Personal Items, Description: Personal Item, Date submitted: None, Type: Passport, Color: Red"
        )
        self.owner_details = {
            "name": "name",
            "surname": "surname",
            "email": "owner@domain.com",
            "role": "user"
        }

    @patch("webapp.service.matches_service.select_matches_by_item")
    @patch("webapp.service.matches_service.select_items_by_email")
    def test_get_unconfirmed_matches_success(self, mock_select_items_by_email, mock_select_matches_by_item):
        mock_select_items_by_email.return_value = [self.found_item]
        mock_select_matches_by_item.return_value = [self.unconfirmed_match]

        result = get_unconfirmed_matches(self.found_item.email)
        mock_select_items_by_email.assert_called_once_with(self.found_item.email)
        mock_select_matches_by_item.assert_called_once_with(self.found_item)
        self.assertEqual(result, [{
            "match_id": "1",
            "synopsis": "Red Passport"
        }])

    @patch("webapp.service.matches_service.select_items_by_email")
    def test_get_unconfirmed_matches_fail_email(self, mock_select_items_by_email):
        mock_select_items_by_email.return_value = []

        result = get_unconfirmed_matches(self.found_item.email)
        mock_select_items_by_email.assert_called_once_with(self.found_item.email)
        self.assertFalse(result)

    @patch("webapp.service.matches_service.select_match_by_id")
    def test_unconfirmed_match_success(self, mock_select_match_by_id):
        mock_select_match_by_id.return_value = self.unconfirmed_match
        result = get_unconfirmed_match("1")
        self.assertEqual(result, {
            "match_id": "1",
            "lost": {
                "id": "2",
                "category": "Personal Items",
                "status": "lost",
                "description": "Personal Item",
                "created_at": "None",
                "email": "owner@domain.com",
                "item_type": "Passport",
                "attributes": {
                    "color": "Red"
                }
            },
            "found": {
                "id": "1",
                "category": "Personal Items",
                "status": "found",
                "description": "Personal Item",
                "created_at": "None",
                "email": "found@domain.com",
                "item_type": "Passport",
                "attributes": {
                    "color": "Red"
                }
            },
            "percentage": "100"
        })

    @patch("webapp.service.matches_service.get_user_account_details")
    @patch("webapp.service.matches_service.select_matches_by_item")
    @patch("webapp.service.matches_service.select_items_by_email")
    def test_get_confirmed_matches_with_owner_info_success(self, mock_select_items_by_email, mock_select_matches_by_item, mock_get_user_account_details):
        mock_select_items_by_email.return_value = [self.found_item]
        mock_select_matches_by_item.return_value = [self.confirmed_match]
        mock_get_user_account_details.return_value = self.owner_details

        result = get_confirmed_matches_with_owner_info(self.found_item.email)
        mock_select_items_by_email.assert_called_once_with(self.found_item.email)
        mock_select_matches_by_item.assert_called_once_with(self.found_item)
        mock_get_user_account_details.assert_called_once_with(self.lost_item.email)
        self.assertEqual(result, [{
            "match_id": "2",
            "found": {
                "id": "1",
                "category": "Personal Items",
                "status": "found",
                "description": "Personal Item",
                "created_at": "None",
                "email": "found@domain.com",
                "item_type": "Passport",
                "attributes": {
                    "color": "Red"
                }
            },
            "owner": self.owner_details
        }])

    @patch("webapp.service.matches_service.select_items_by_email")
    def test_get_confirmed_matches_with_owner_info_fail_email(self, mock_select_items_by_email):
        mock_select_items_by_email.return_value = []

        result = get_confirmed_matches_with_owner_info(self.found_item.email)
        mock_select_items_by_email.assert_called_once_with(self.found_item.email)
        self.assertFalse(result)

    @patch("webapp.service.matches_service.insert_update_match")
    @patch("webapp.service.matches_service.select_match_by_id")
    def test_confirm_match(self, mock_select_match_by_id, mock_insert_update_match):
        mock_select_match_by_id.return_value = self.unconfirmed_match

        result = confirm_match(str(self.unconfirmed_match.id))

        mock_select_match_by_id.assert_called_once_with(self.unconfirmed_match.id)
        self.unconfirmed_match.status = MatchStatusEnum.CONFIRMED
        mock_insert_update_match.assert_called_once_with(self.unconfirmed_match)
        self.assertTrue(result)

    @patch("webapp.service.matches_service.generate_pickup_report")
    @patch("webapp.service.matches_service.insert_update_match")
    @patch("webapp.service.matches_service.insert_update_item")
    @patch("webapp.service.matches_service.get_user_account_details")
    @patch("webapp.service.matches_service.select_match_by_id")
    def test_hand_over_and_archive_match_success_receipt(self, mock_select_match_by_id, mock_get_user_account_details,
                                                  mock_insert_update_item, mock_insert_update_match, mock_generate_pickup_report):
        mock_select_match_by_id.return_value = self.confirmed_match
        mock_get_user_account_details.return_value = self.owner_details
        mock_generate_pickup_report.return_value = "base64_encoded_pdf"

        result = hand_over_and_archive_match(str(self.confirmed_match.id), "12345678910", True)
        
        mock_select_match_by_id.assert_called_once_with(self.confirmed_match.id)
        mock_get_user_account_details.assert_called_once_with(self.lost_item.email)
        mock_insert_update_item.assert_called_once_with(self.archive_item)
        self.confirmed_match.status = MatchStatusEnum.PICKED_UP
        mock_insert_update_match.assert_called_once_with(self.confirmed_match)
        self.owner_details["pesel"] = "12345678910"
        mock_generate_pickup_report.assert_called_once_with(self.owner_details, self.found_item.to_dict())

        expected_result = "base64_encoded_pdf"
        self.assertEqual(expected_result, result)

    @patch("webapp.service.matches_service.insert_update_match")
    @patch("webapp.service.matches_service.insert_update_item")
    @patch("webapp.service.matches_service.get_user_account_details")
    @patch("webapp.service.matches_service.select_match_by_id")
    def test_hand_over_and_archive_match_success_no_receipt(self, mock_select_match_by_id, mock_get_user_account_details,
                                                  mock_insert_update_item, mock_insert_update_match):
        mock_select_match_by_id.return_value = self.confirmed_match
        mock_get_user_account_details.return_value = self.owner_details

        result = hand_over_and_archive_match(str(self.confirmed_match.id), "12345678910", False)
        
        mock_select_match_by_id.assert_called_once_with(self.confirmed_match.id)
        mock_get_user_account_details.assert_called_once_with(self.lost_item.email)
        mock_insert_update_item.assert_called_once_with(self.archive_item)
        self.confirmed_match.status = MatchStatusEnum.PICKED_UP
        mock_insert_update_match.assert_called_once_with(self.confirmed_match)

        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()