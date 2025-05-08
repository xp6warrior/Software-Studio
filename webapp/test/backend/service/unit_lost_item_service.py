import unittest
from unittest.mock import patch
import webapp.models.models as model
import webapp.models.enums as enums
from webapp.backend.service.lost_item_service import *

class TestGetSubmittedLostItems(unittest.TestCase):
    @patch("webapp.backend.service.lost_item_service.select_items")
    def test_get_submitted_lost_items_success(self, mock_select_items):
        mock_select_items.return_value = [
            models.PersonalItems(
                id=5,
                type=enums.PersonalItemType.KEYS,
                color=enums.ColorEnum.GREEN,
                description="Small key",
                status=enums.StatusEnum.LOST,
                email="test@test.com"
            ),
            models.Jewelry(
                id=7,
                type=enums.JewelryType.NECKLACE,
                color=enums.ColorEnum.BLUE,
                size=enums.SizeEnum.XS,
                description="My necklace",
                status=enums.StatusEnum.LOST,
                email="test@test.com"
            )
        ]
        items = get_submitted_lost_items("test@test.com")
        mock_select_items.assert_called_once_with("test@test.com")

        self.assertEqual(items, [
            {
                "Item": {
                    "id": 5,
                    "type": "keys",
                    "color": "green",
                    "description": "Small key"
                },
                "status": "lost"
            },
            {
                "Item": {
                    "id": 7,
                    "type": "necklace",
                    "color": "blue",
                    "size": "xs",
                    "description": "My necklace"
                },
                "status": "lost"
            }
        ])

class TestSubmitLostItem(unittest.TestCase):
    @patch('webapp.backend.service.lost_item_service.insert_update_item')
    def test_submit_lost_item_success(self, mock_insert_update_item):
        email = "abc@123.com"
        personal_item_json = {
            "model": "personalitems",
            "type": "keys",
            "color": "green",
            "description": "Small key",
            "status": "lost"
        }
        personal_item_obj = model.PersonalItems(
            type=enums.PersonalItemType.KEYS,
            color=enums.ColorEnum.GREEN,
            description="Small key",
            status=enums.StatusEnum.LOST,
            email=email
        )
        submit_lost_item(email, personal_item_json)
        mock_insert_update_item.assert_called_once_with(personal_item_obj)


class TestEditSubmittedLostItem(unittest.TestCase):
    @patch('webapp.backend.service.lost_item_service.insert_update_item')
    def test_edit_submitted_lost_item_success(self, mock_insert_update_item):
        accessory_json = {
            "model": "accessories",
            "type": "glasses",
            "color": "red",
            "material": "plastic",
            "brand": "Poloriod",
            "description": "My awesome glasses pls find",
            "status": "lost"
        }
        accessory_obj = model.Accessories(
            id=5,
            type=enums.AccessoryType.GLASSES,
            color=enums.ColorEnum.RED,
            material=enums.MaterialEnum.PLASTIC,
            brand="Poloriod",
            description="My awesome glasses pls find",
            status=enums.StatusEnum.LOST,
            email="abc@123.com"
        )

        edit_submitted_lost_item(5, "abc@123.com", accessory_json)
        mock_insert_update_item.assert_called_once_with(accessory_obj)

class TestDeleteSubmittedLostItem(unittest.TestCase):
    @patch('webapp.backend.service.lost_item_service.delete_item')
    def test_delete_submitted_lost_item_success(self, mock_delete_item):
        delete_submitted_lost_item(5, "test@test.com", "accessories")
        mock_delete_item.assert_called_once_with(models.Accessories, 5, "test@test.com")

    # Exception on invalid model class
    @patch('webapp.backend.service.lost_item_service.delete_item')
    def test_delete_submitted_lost_item_success(self, mock_delete_item):
        with self.assertRaises(Exception) as context:
            delete_submitted_lost_item(5, "test@test.com", "fake_model_name")

        self.assertEqual(str(context.exception), "Invalid model class! fake_model_name")

class TestCreateModelFromJson(unittest.TestCase):
    # Success with: unordered attributes, case insensitive keys, invalid attributes
    def test_create_model_from_json_success(self):
        travel_item_json = {
            "material": "leather",
            "moDEl": "travelitems",
            "email": "abc@123.com",
            "TYPE": "suitcase",
            
            # Invalid attributes
            "id": "10",
            "fake_attribute": "value"
        }
        travel_item_obj = model.TravelItems(
            type=enums.TravelItemType.SUITCASE,
            material=enums.MaterialEnum.LEATHER,
            email="abc@123.com"
        )

        actual_obj = create_model_from_json(travel_item_json)
        self.assertEqual(travel_item_obj, actual_obj)

    # Exception when no model specified
    def test_create_model_from_json_no_model(self):
        jewelry_json = {
            "type": "ring",
            "color": "blue",
            "size": "xs",
            "description": "Small ring",
            "status": "lost",
            "email": "abc@123.com"
        }
    
        with self.assertRaises(Exception) as context:
            create_model_from_json(jewelry_json)

        self.assertEqual(str(context.exception), "\"model\" attribute must be defined!")

    # Exception when invalid model class
    def test_submit_lost_item_invalid_model(self):
        medicine_json = {
            "model": "accounts",
            "type": "pills",
            "color": "white",
            "size": "xs",
            "description": "My pills",
            "status": "lost",
            "email": "abc@123.com"
        }
    
        with self.assertRaises(Exception) as context:
            create_model_from_json(medicine_json)

        self.assertEqual(str(context.exception), "Invalid model class! accounts")


if __name__ == "__main__":
    unittest.main()