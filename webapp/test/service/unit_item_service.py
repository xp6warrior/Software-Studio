import unittest
from unittest.mock import patch, call
from webapp.models2.models import PersonalItems, Matches
from webapp.models2.enums import PersonalItemType, ColorEnum, MatchStatusEnum
from webapp.service.item_service import *

class TestItemService(unittest.TestCase):

    def setUp(self):
        self.lost_item = PersonalItems(
            id=1, type=PersonalItemType.KEYS, color=ColorEnum.GREEN,
            description="Small key", status=StatusEnum.LOST, email="test@test.com"
        )
        self.found_item = PersonalItems(
            id=2, type=PersonalItemType.KEYS, color=ColorEnum.GREEN,
            description="Small key", status=StatusEnum.FOUND, email="test@test.com"
        )
        self.match = Matches(
            id=1, status=MatchStatusEnum.UNCONFIRMED, percentage=100, lost_item=self.lost_item,
            found_item=self.found_item
        )
        self.match2 = Matches(
            id=2, status=MatchStatusEnum.UNCONFIRMED, percentage=80, lost_item=self.lost_item,
            found_item=self.found_item
        )

    @patch("webapp.service.item_service.select_matches_by_item")
    @patch("webapp.service.item_service.select_items_by_email")
    def test_get_submitted_items_success_pending(self, mock_select_items_by_email, mock_select_matches_by_item):
        mock_select_items_by_email.return_value = [self.lost_item]
        mock_select_matches_by_item.return_value = []

        result = get_submitted_lost_items("test@test.com")
        mock_select_items_by_email.assert_called_once_with("test@test.com")
        mock_select_matches_by_item.assert_called_once_with(self.lost_item)

        self.assertEqual(result, [{
            "id": "1",
            "category": "Personal Items",
            "status": "Pending",
            "desc": "Small key",
            "created_at": "None",
            "email": "test@test.com",
            "it": "Keys",
            "color": "Green"
        }])

    @patch("webapp.service.item_service.select_matches_by_item")
    @patch("webapp.service.item_service.select_items_by_email")
    def test_get_submitted_items_success_under_review(self, mock_select_items_by_email, mock_select_matches_by_item):
        mock_select_items_by_email.return_value = [self.lost_item]
        mock_select_matches_by_item.return_value = [self.match, self.match2]
        expected_result = [{
            "id": "1",
            "category": "Personal Items",
            "status": "Under review",
            "desc": "Small key",
            "created_at": "None",
            "email": "test@test.com",
            "it": "Keys",
            "color": "Green"
        }]

        result = get_submitted_lost_items("test@test.com")
        self.assertEqual(result, expected_result)

        self.match.status = MatchStatusEnum.DECLINED
        result = get_submitted_lost_items("test@test.com")
        self.assertEqual(result, expected_result)

        self.match.status = MatchStatusEnum.FALSE_PICKUP
        result = get_submitted_lost_items("test@test.com")
        self.assertEqual(result, expected_result)

        mock_select_items_by_email.assert_has_calls([call("test@test.com"), call("test@test.com"), call("test@test.com")])
        mock_select_matches_by_item.assert_has_calls([call(self.lost_item), call(self.lost_item), call(self.lost_item)])

    @patch("webapp.service.item_service.select_matches_by_item")
    @patch("webapp.service.item_service.select_items_by_email")
    def test_get_submitted_items_success_matched(self, mock_select_items_by_email, mock_select_matches_by_item):
        mock_select_items_by_email.return_value = [self.lost_item]
        self.match.status = MatchStatusEnum.CONFIRMED
        mock_select_matches_by_item.return_value = [self.match, self.match2]

        result = get_submitted_lost_items("test@test.com")
        mock_select_items_by_email.assert_called_once_with("test@test.com")
        mock_select_matches_by_item.assert_called_once_with(self.lost_item)

        self.assertEqual(result, [{
            "id": "1",
            "category": "Personal Items",
            "status": "Matched",
            "desc": "Small key",
            "created_at": "None",
            "email": "test@test.com",
            "it": "Keys",
            "color": "Green"
        }])

    @patch("webapp.service.item_service.select_matches_by_item")
    @patch("webapp.service.item_service.select_items_by_email")
    def test_get_submitted_items_success_picked_up(self, mock_select_items_by_email, mock_select_matches_by_item):
        mock_select_items_by_email.return_value = [self.lost_item]
        self.match.status = MatchStatusEnum.PICKED_UP
        mock_select_matches_by_item.return_value = [self.match, self.match2]

        result = get_submitted_lost_items("test@test.com")
        mock_select_items_by_email.assert_called_once_with("test@test.com")
        mock_select_matches_by_item.assert_called_once_with(self.lost_item)

        self.assertEqual(result, [{
            "id": "1",
            "category": "Personal Items",
            "status": "Picked up",
            "desc": "Small key",
            "created_at": "None",
            "email": "test@test.com",
            "it": "Keys",
            "color": "Green"
        }])

    @patch("webapp.service.item_service.delete_image")
    @patch("webapp.service.item_service.delete_item")
    @patch("webapp.service.item_service.select_item_by_id")
    def test_delete_lost_item_success(self, mock_select_item_by_id, mock_delete_item, mock_delete_image):
        mock_select_item_by_id.return_value = self.lost_item

        result = delete_lost_item("test@test.com", "1")
        mock_select_item_by_id.assert_called_once_with(1)
        mock_delete_item.assert_called_once_with(1)
        mock_delete_image.assert_called_once_with(None)
        self.assertTrue(result)

    @patch("webapp.service.item_service.select_item_by_id")
    def test_delete_lost_item_fail(self, mock_select_item_by_id):
        mock_select_item_by_id.return_value = None
        result = delete_lost_item("test@test.com", "1")
        self.assertFalse(result)

        mock_select_item_by_id.return_value = self.lost_item
        result = delete_lost_item("test2@domain.com", "1")
        self.assertFalse(result)

        mock_select_item_by_id.assert_has_calls([call(1), call(1)])


    # @patch("webapp.service.item_service.select_matches")
    # @patch("webapp.service.item_service.select_items")
    # def test_get_submitted_items(self, mock_select_items, mock_select_matches):
    #     personal_item = PersonalItems(
    #         id=5, type=PersonalItemType.KEYS, color=ColorEnum.GREEN,
    #         description="Small key", status=StatusEnum.LOST, email="test@test.com"
    #     )
    #     jewelry = Jewelry(
    #         id=7, type=JewelryType.NECKLACE, color=ColorEnum.BLUE,
    #         size=SizeEnum.XS, description="My necklace", status=StatusEnum.LOST,
    #         email="test@test.com"
    #     )
    #     match1 = Match(
    #         id=1, table_name="personalitems", lost_item_id=3, found_item_id=5,
    #         status=MatchStatus.UNCONFIRMED
    #     )
    #     match2 = Match(
    #         id=2, table_name="jewelry", lost_item_id=5, found_item_id=7,
    #         status=MatchStatus.CONFIRMED
    #     )
    #     personal_item_item = Lost_Item(
    #         "personalitems", "keys", "green", "Small key", None, None, None, None, "lost", "5"
    #     )
    #     jewelry_item = Lost_Item(
    #         "jewelry", "necklace", "blue", "My necklace", "xs", None, None, None, "confirmed", "7"
    #     )
    #     mock_select_items.side_effect = [[personal_item, jewelry], []]
    #     mock_select_matches.side_effect = [[match1], [match2]]
        
    #     # 2 models
    #     items = get_submitted_lost_items("test@test.com")
    #     self.assertCountEqual(items, [personal_item_item, jewelry_item])

    #     # No models
    #     items = get_submitted_lost_items("other@other.com")
    #     self.assertEqual(items, [])

    #     # Mock assertions
    #     mock_select_items.assert_has_calls([call("test@test.com"), call("other@other.com")])
    #     mock_select_matches.assert_has_calls([
    #         call(personal_item.id, PersonalItems), call(jewelry.id, Jewelry)
    #     ])

    #     # Exception
    #     with self.assertRaises(Exception) as context:
    #         get_submitted_lost_items("not an email@ase")
    #     self.assertEqual(str(context.exception), "Invalid email address! not an email@ase")


    # @patch("webapp.service.item_service.insert_update_item")
    # def test_submit_lost_item(self, mock_select_items):
    #     accessory = Accessories(
    #         type=AccessoryType.GLASSES, color=ColorEnum.BLACK, material=MaterialEnum.PLASTIC,
    #         brand="", description="Cool glasses", status=StatusEnum.LOST, email="test@test.com"
    #     )
    #     accessory_item = Lost_Item(
    #         "accessories", "glasses", "black", "Cool glasses", None, "plastic", "", None, "lost", None
    #     )
    #     accessory_item2 = Lost_Item(
    #         "accessory", "glasses", "black", "Cool glasses", None, "plastic", "", None, "lost", None
    #     )

    #     submit_lost_item(accessory.email, accessory_item)
    #     mock_select_items.assert_called_once_with(accessory)

    #     # Exception
    #     with self.assertRaises(Exception) as context:
    #         submit_lost_item(accessory.email, accessory_item2)
    #     self.assertEqual(str(context.exception), "Invalid item cateogory! accessory")

    # @patch("webapp.service.item_service.insert_update_item")
    # def test_submit_found_item(self, mock_select_items):
    #     accessory = Accessories(
    #         type=AccessoryType.GLASSES, color=ColorEnum.BLACK, material=MaterialEnum.PLASTIC,
    #         brand="", description="Cool glasses", status=StatusEnum.FOUND, email="test@test.com"
    #     )
    #     accessory_item = Found_Item(
    #         "accessories", "glasses", "black", "Cool glasses", None, "plastic", "", None, None
    #     )
    #     accessory_item2 = Found_Item(
    #         "accessory", "glasses", "black", "Cool glasses", None, "plastic", "", None, None
    #     )

    #     submit_found_item(accessory.email, accessory_item)
    #     mock_select_items.assert_called_once_with(accessory)

    #     # Exception
    #     with self.assertRaises(Exception) as context:
    #         submit_found_item(accessory.email, accessory_item2)
    #     self.assertEqual(str(context.exception), "Invalid item cateogory! accessory")

    # @patch("webapp.service.item_service.delete_item")
    # @patch("webapp.service.item_service.select_item_by_id")
    # def test_delete_lost_item(self, mock_select_item_by_id, mock_delete_item):
    #     personal_item = PersonalItems(
    #         id=5, type=PersonalItemType.KEYS, color=ColorEnum.GREEN,
    #         description="Small key", status=StatusEnum.LOST, email="test@test.com"
    #     )
    #     mock_select_item_by_id.return_value = personal_item
    #     delete_lost_item(personal_item.email, personal_item.id, PersonalItems)
    #     mock_select_item_by_id.assert_called_once_with(5, PersonalItems)
    #     mock_delete_item.assert_called_once_with(personal_item)

    #     # Exception
    #     with self.assertRaises(Exception) as context:
    #         delete_lost_item("other@other.com", personal_item.id, PersonalItems)
    #     self.assertEqual(str(context.exception), "Attempt to delete item of other user!")

    #     mock_select_item_by_id.return_value = None
    #     with self.assertRaises(Exception) as context:
    #         delete_lost_item("example@other.com", 5, str)
    #     self.assertEqual(str(context.exception), "str of id 5 does not exist!")

    # @patch("webapp.service.item_service.insert_update_item")
    # @patch("webapp.service.item_service.select_account")
    # @patch("webapp.service.item_service.select_matches")
    # @patch("webapp.service.item_service.select_item_by_id")
    # def test_hand_over_and_archive_match(self, mock_select_item_by_id, mock_select_matches,
    #                                      mock_select_account, mock_insert_update_item):
    #     personal_item_found = PersonalItems(
    #         id=5, type=PersonalItemType.KEYS, color=ColorEnum.GREEN,
    #         description="Small key", status=StatusEnum.FOUND, email="worker@test.com"
    #     )
    #     personal_item_lost = PersonalItems(
    #         id=3, type=PersonalItemType.KEYS, color=ColorEnum.GREEN,
    #         description="Small key", status=StatusEnum.LOST, email="user@test.com"
    #     )
    #     match1 = Match(
    #         id=1, table_name="personalitems", lost_item_id=3, found_item_id=5,
    #         status=MatchStatus.CONFIRMED, percentage=90
    #     )
    #     match2 = Match(
    #         id=3, table_name="personalitems", lost_item_id=6, found_item_id=5,
    #         status=MatchStatus.UNCONFIRMED, percentage=70
    #     )
    #     account = Accounts(
    #         id=1, email="user@test.com", password="password", role=RoleEnum.USER, pesel=12345,
    #         name="name", surname="surname"
    #     )
    #     archived_item = ArchivePersonalItems(
    #         id=5, type=PersonalItemType.KEYS, color=ColorEnum.GREEN, description="Small key",
    #         email="user@test.com", username="name", surname="surname", pesel=12345
    #     )
    #     mock_select_item_by_id.side_effect = [personal_item_found, personal_item_lost]
    #     mock_select_matches.return_value = [match1, match2]
    #     mock_select_account.return_value = account

    #     hand_over_and_archive_match(5, PersonalItems)
    #     mock_select_item_by_id.assert_has_calls([call(5, PersonalItems), call(3, PersonalItems)])
    #     mock_select_matches.assert_called_once_with(5, PersonalItems)
    #     mock_select_account.assert_called_once_with("user@test.com")
    #     mock_insert_update_item.assert_called_once_with(archived_item)

if __name__ == "__main__":
    unittest.main()