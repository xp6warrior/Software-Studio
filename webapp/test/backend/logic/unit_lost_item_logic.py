import unittest
from unittest.mock import patch
import webapp.models.models as model
import webapp.models.enums as enums
from webapp.backend.logic.lost_item_logic import *

class TestSubmitLostItem(unittest.TestCase):
    # Success
    @patch('webapp.backend.logic.lost_item_logic.insert_item')
    def test_submit_lost_item_success(self, mock_insert_item):
        email = "abc@123.com"
        personal_item_json = {
            "model": "personalitems",
            "type": "keys",
            "color": "green",
            "description": "Small ring",
            "status": "lost"
        }
        personal_item_obj = model.PersonalItems(
            type=enums.PersonalItemType.KEYS,
            color=enums.ColorEnum.GREEN,
            description="Small ring",
            status=enums.StatusEnum.LOST,
            email=email
        )
        submit_lost_item(email, personal_item_json)
        mock_insert_item.assert_called_once_with(personal_item_obj)


class TestEditLostItem(unittest.TestCase):
    # Success
    @patch('webapp.backend.logic.lost_item_logic.update_item')
    def test_edit_submitted_lost_item_success(self, mock_logic_update_item):
        accessory_json = {
            "model": "accessories",
            "type": "glasses",
            "color": "red",
            "material": "plastic",
            "brand": "Poloriod",
            "description": "My awesome classes pls find",
            "status": "lost"
        }
        accessory_obj = model.Accessories(
            id=5,
            type=enums.AccessoryType.GLASSES,
            color=enums.ColorEnum.RED,
            material=enums.MaterialEnum.PLASTIC,
            brand="Poloriod",
            description="My awesome classes pls find",
            status=enums.StatusEnum.LOST,
            email="abc@123.com"
        )

        edit_submitted_lost_item(5, "abc@123.com", accessory_json)
        mock_logic_update_item.assert_called_once_with(accessory_obj, model.Accessories, 5, "abc@123.com")


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
    def test_submit_lost_iteminvalid_model(self):
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