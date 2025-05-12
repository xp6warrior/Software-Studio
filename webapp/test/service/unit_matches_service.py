import unittest
from unittest.mock import patch
from webapp.service.matches_service import *
from webapp.models.models import *
from webapp.models.enums import *
from webapp.items import *

class TestMatchesService(unittest.TestCase):

    @patch("webapp.service.matches_service.select_item_by_id")
    @patch("webapp.service.matches_service.select_matches")
    @patch("webapp.service.matches_service.select_items")
    def test_get_matches(self, mock_select_items, mock_select_matches, mock_select_item_by_id):
        lost_jewelry = Jewelry(
            id=1, type=JewelryType.NECKLACE, color=ColorEnum.RED, size=SizeEnum.XS,
            description="My necklace", status=StatusEnum.LOST, email="lost@user.com"
        )
        found_jewelry = Jewelry(
            id=2, type=JewelryType.NECKLACE, color=ColorEnum.RED, size=SizeEnum.XS,
            status=StatusEnum.FOUND, email="found@worker.com"
        )
        match1 = Match(
            id=1, table_name="jewelry", found_item_id=2, lost_item_id=1, status=MatchStatus.UNCONFIRMED
        )
        match2 = Match(
            id=2, table_name="jewelry", found_item_id=2, lost_item_id=3, status=MatchStatus.CONFIRMED
        )
        lost_item = Lost_Item(
            "jewelry", "necklace", "red", "My necklace", "xs", None, None, None, "lost", "1"
        )
        found_item = Found_Item(
            "jewelry", "necklace", "red", None, "xs", None, None, None, "2"
        )

        mock_select_items.return_value = [found_jewelry]
        mock_select_matches.return_value = [match1, match2]
        mock_select_item_by_id.return_value = lost_jewelry

        matches = get_matches("found@worker.com")
        mock_select_items.assert_called_once_with("found@worker.com")
        mock_select_matches.assert_called_once_with(2, Jewelry)
        mock_select_item_by_id.assert_called_once_with(1, Jewelry)
        self.assertEqual(matches, [[lost_item, found_item, "Schema doesn't store percentage yet :P"]])

        mock_select_items.return_value = []
        matches = get_matches("other@worker.com")
        self.assertEqual(matches, [])

    @patch("webapp.service.matches_service.insert_update_match")
    @patch("webapp.service.matches_service.select_matches")
    def test_confirm_match(self, mock_select_matches, mock_insert_update_match):
        match1 = Match(
            id=1, table_name="jewelry", found_item_id=2, lost_item_id=1, status=MatchStatus.UNCONFIRMED
        )
        match2 = Match(
            id=2, table_name="jewelry", found_item_id=2, lost_item_id=3, status=MatchStatus.CONFIRMED
        )
        mock_select_matches.return_value = [match1, match2]

        confirm_match(1, 2, Jewelry)
        mock_select_matches.assert_called_once_with(2, Jewelry)
        mock_insert_update_match.assert_called_once_with(match1)

    @patch("webapp.service.matches_service.select_account")
    @patch("webapp.service.matches_service.select_item_by_id")
    @patch("webapp.service.matches_service.select_matches")
    @patch("webapp.service.matches_service.select_items")
    def test_get_confirmed_matches_with_user_pesel(self, mock_select_items, mock_select_matches,
                                                   mock_select_item_by_id, mock_select_account):
        lost_jewelry = Jewelry(
            id=3, type=JewelryType.NECKLACE, color=ColorEnum.RED, size=SizeEnum.XS,
            description="My necklace", status=StatusEnum.LOST, email="lost@user.com"
        )
        found_jewelry = Jewelry(
            id=2, type=JewelryType.NECKLACE, color=ColorEnum.RED, size=SizeEnum.XS,
            status=StatusEnum.FOUND, email="found@worker.com"
        )
        account = Accounts(
            email="lost@user.com", password="password", role=RoleEnum.USER, pesel=12345
        )
        match1 = Match(
            id=1, table_name="jewelry", found_item_id=2, lost_item_id=1, status=MatchStatus.UNCONFIRMED
        )
        match2 = Match(
            id=2, table_name="jewelry", found_item_id=2, lost_item_id=3, status=MatchStatus.CONFIRMED
        )
        matched_item = Matched_Item(
            "jewelry", "necklace", "red", "My necklace", "xs", None, None, None, "3", "12345"
        )
        mock_select_items.return_value = [found_jewelry]
        mock_select_matches.return_value = [match1, match2]
        mock_select_item_by_id.return_value = lost_jewelry
        mock_select_account.return_value = account

        result = get_confirmed_matches_with_user_pesel("found@worker.com")
        mock_select_items.assert_called_once_with("found@worker.com")
        mock_select_matches.assert_called_once_with(2, Jewelry)
        mock_select_item_by_id.assert_called_once_with(3, Jewelry)
        mock_select_account.assert_called_once_with("lost@user.com")
        self.assertEqual(result, [matched_item])

if __name__ == "__main__":
    unittest.main()