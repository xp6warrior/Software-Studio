import unittest
from unittest.mock import patch, call
from webapp.models.models import *
from webapp.models.enums import *
from webapp.service.item_service import *

class TestItemService(unittest.TestCase):

    @patch("webapp.service.item_service.select_matches")
    @patch("webapp.service.item_service.select_items")
    def test_get_submitted_items(self, mock_select_items, mock_select_matches):
        personal_item = PersonalItems(
            id=5, type=PersonalItemType.KEYS, color=ColorEnum.GREEN,
            description="Small key", status=StatusEnum.LOST, email="test@test.com"
        )
        jewelry = Jewelry(
            id=7, type=JewelryType.NECKLACE, color=ColorEnum.BLUE,
            size=SizeEnum.XS, description="My necklace", status=StatusEnum.LOST,
            email="test@test.com"
        )
        match1 = Match(
            id=1, table_name="personalitems", lost_item_id=3, found_item_id=5,
            status=MatchStatus.UNCONFIRMED
        )
        match2 = Match(
            id=2, table_name="jewelry", lost_item_id=5, found_item_id=7,
            status=MatchStatus.CONFIRMED
        )
        personal_item_item = Lost_Item(
            "personalitems", "keys", "green", "Small key", None, None, None, None, "lost", "5"
        )
        jewelry_item = Lost_Item(
            "jewelry", "necklace", "blue", "My necklace", "xs", None, None, None, "confirmed", "7"
        )
        mock_select_items.side_effect = [[personal_item, jewelry], []]
        mock_select_matches.side_effect = [[match1], [match2]]
        
        # 2 models
        items = get_submitted_lost_items("test@test.com")
        self.assertCountEqual(items, [personal_item_item, jewelry_item])

        # No models
        items = get_submitted_lost_items("other@other.com")
        self.assertEqual(items, [])

        # Mock assertions
        mock_select_items.assert_has_calls([call("test@test.com"), call("other@other.com")])
        mock_select_matches.assert_has_calls([
            call(personal_item.id, PersonalItems), call(jewelry.id, Jewelry)
        ])

        # Exception
        with self.assertRaises(Exception) as context:
            get_submitted_lost_items("not an email@ase")
        self.assertEqual(str(context.exception), "Invalid email address! not an email@ase")


    @patch("webapp.service.item_service.insert_update_item")
    def test_submit_lost_item(self, mock_select_items):
        accessory = Accessories(
            type=AccessoryType.GLASSES, color=ColorEnum.BLACK, material=MaterialEnum.PLASTIC,
            brand="", description="Cool glasses", status=StatusEnum.LOST, email="test@test.com"
        )
        accessory_item = Lost_Item(
            "accessories", "glasses", "black", "Cool glasses", None, "plastic", "", None, "lost", None
        )
        accessory_item2 = Lost_Item(
            "accessory", "glasses", "black", "Cool glasses", None, "plastic", "", None, "lost", None
        )

        submit_lost_item(accessory.email, accessory_item)
        mock_select_items.assert_called_once_with(accessory)

        # Exception
        with self.assertRaises(Exception) as context:
            submit_lost_item(accessory.email, accessory_item2)
        self.assertEqual(str(context.exception), "Invalid item cateogory! accessory")

    @patch("webapp.service.item_service.insert_update_item")
    def test_submit_found_item(self, mock_select_items):
        accessory = Accessories(
            type=AccessoryType.GLASSES, color=ColorEnum.BLACK, material=MaterialEnum.PLASTIC,
            brand="", description="Cool glasses", status=StatusEnum.FOUND, email="test@test.com"
        )
        accessory_item = Found_Item(
            "accessories", "glasses", "black", "Cool glasses", None, "plastic", "", None, None
        )
        accessory_item2 = Found_Item(
            "accessory", "glasses", "black", "Cool glasses", None, "plastic", "", None, None
        )

        submit_found_item(accessory.email, accessory_item)
        mock_select_items.assert_called_once_with(accessory)

        # Exception
        with self.assertRaises(Exception) as context:
            submit_found_item(accessory.email, accessory_item2)
        self.assertEqual(str(context.exception), "Invalid item cateogory! accessory")

    @patch("webapp.service.item_service.delete_item")
    @patch("webapp.service.item_service.select_item_by_id")
    def test_delete_lost_item(self, mock_select_item_by_id, mock_delete_item):
        personal_item = PersonalItems(
            id=5, type=PersonalItemType.KEYS, color=ColorEnum.GREEN,
            description="Small key", status=StatusEnum.LOST, email="test@test.com"
        )
        mock_select_item_by_id.return_value = personal_item
        delete_lost_item(personal_item.email, personal_item.id, PersonalItems)
        mock_select_item_by_id.assert_called_once_with(5, PersonalItems)
        mock_delete_item.assert_called_once_with(personal_item)

        # Exception
        with self.assertRaises(Exception) as context:
            delete_lost_item("other@other.com", personal_item.id, PersonalItems)
        self.assertEqual(str(context.exception), "Attempt to delete item of other user!")

        mock_select_item_by_id.return_value = None
        with self.assertRaises(Exception) as context:
            delete_lost_item("example@other.com", 5, str)
        self.assertEqual(str(context.exception), "str of id 5 does not exist!")

    @patch("webapp.service.item_service.insert_update_item")
    @patch("webapp.service.item_service.select_account")
    @patch("webapp.service.item_service.select_matches")
    @patch("webapp.service.item_service.select_item_by_id")
    def test_hand_over_and_archive_match(self, mock_select_item_by_id, mock_select_matches,
                                         mock_select_account, mock_insert_update_item):
        personal_item_found = PersonalItems(
            id=5, type=PersonalItemType.KEYS, color=ColorEnum.GREEN,
            description="Small key", status=StatusEnum.FOUND, email="worker@test.com"
        )
        personal_item_lost = PersonalItems(
            id=3, type=PersonalItemType.KEYS, color=ColorEnum.GREEN,
            description="Small key", status=StatusEnum.LOST, email="user@test.com"
        )
        match1 = Match(
            id=1, table_name="personalitems", lost_item_id=3, found_item_id=5,
            status=MatchStatus.CONFIRMED, percentage=90
        )
        match2 = Match(
            id=3, table_name="personalitems", lost_item_id=6, found_item_id=5,
            status=MatchStatus.UNCONFIRMED, percentage=70
        )
        account = Accounts(
            id=1, email="user@test.com", password="password", role=RoleEnum.USER, pesel=12345,
            name="name", surname="surname"
        )
        archived_item = ArchivePersonalItems(
            id=5, type=PersonalItemType.KEYS, color=ColorEnum.GREEN, description="Small key",
            email="user@test.com", username="name", surname="surname", pesel=12345
        )
        mock_select_item_by_id.side_effect = [personal_item_found, personal_item_lost]
        mock_select_matches.return_value = [match1, match2]
        mock_select_account.return_value = account

        hand_over_and_archive_match(5, PersonalItems)
        mock_select_item_by_id.assert_has_calls([call(5, PersonalItems), call(3, PersonalItems)])
        mock_select_matches.assert_called_once_with(5, PersonalItems)
        mock_select_account.assert_called_once_with("user@test.com")
        mock_insert_update_item.assert_called_once_with(archived_item)

if __name__ == "__main__":
    unittest.main()