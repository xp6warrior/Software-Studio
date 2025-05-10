import unittest
import reflex
import webapp.models.models as models
import webapp.models.enums as enums
from webapp.repository.item_repo import *
from webapp.service.login_service import create_user

class TestItemRepo(unittest.TestCase):

    def setUp(self):
        create_user("test@test.com", "password", enums.RoleEnum.USER)
        self.personal_item1 = models.PersonalItems(
            type=enums.PersonalItemType.KEYS,
            color=enums.ColorEnum.GRAY,
            description="My keys",
            status=enums.StatusEnum.LOST,
            email="test@test.com"
        )
        self.personal_item2 = models.PersonalItems(
            type=enums.PersonalItemType.CREDIT_DEBIT_CARD,
            color=enums.ColorEnum.WHITE,
            description="My credit card",
            status=enums.StatusEnum.LOST,
            email="test@test.com"
        )
        self.jewelry = models.Jewelry(
            type=enums.JewelryType.NECKLACE,
            color=enums.ColorEnum.RED,
            size=enums.SizeEnum.S,
            description="My necklace",
            status=enums.StatusEnum.LOST,
            email="test@test.com"
        )

    def test_item_crud(self):
        # Insert and select
        insert_update_item(self.jewelry)
        insert_update_item(self.personal_item1)
        insert_update_item(self.personal_item2)
        selected = select_items("test@test.com")
        self.assertCountEqual(selected, [self.jewelry, self.personal_item1, self.personal_item2])

        # Insert exceptions
        with self.assertRaises(Exception) as context:
            insert_update_item(None)
        self.assertEqual(str(context.exception), "insert_update_item parameter must not be None!")
        with self.assertRaises(Exception) as context:
            insert_update_item(5)
        self.assertEqual(str(context.exception), "insert_update_item parameter must be of type Model!")

        # Select exceptions
        with self.assertRaises(Exception) as context:
            select_items(None)
        self.assertEqual(str(context.exception), "select_items parameter must not be None!")
        with self.assertRaises(Exception) as context:
            select_items(5)
        self.assertEqual(str(context.exception), "select_items parameter must be of type str!")

        selected = select_items("other@other.com")
        self.assertEqual(selected, [])

        # Select by id, email
        selected = select_item_by_id_email(self.jewelry.id, "test@test.com", models.Jewelry)
        self.assertEqual(selected, self.jewelry)
        selected = select_item_by_id_email(self.jewelry.id, "test@test.com", models.TravelItems)
        self.assertEqual(selected, None)

        # Select by id, email exceptions
        with self.assertRaises(Exception) as context:
            select_item_by_id_email(None, None, models.Jewelry)
        self.assertEqual(str(context.exception), "select_item_by_id_email id must not be None!")
        with self.assertRaises(Exception) as context:
            select_item_by_id_email("None", None, models.Jewelry)
        self.assertEqual(str(context.exception), "select_item_by_id_email id must be of type int!")
        with self.assertRaises(Exception) as context:
            select_item_by_id_email(5, None, models.Jewelry)
        self.assertEqual(str(context.exception), "select_item_by_id_email email must not be None!")
        with self.assertRaises(Exception) as context:
            select_item_by_id_email(5, 5, models.Jewelry)
        self.assertEqual(str(context.exception), "select_item_by_id_email email must be of type str!")

        # Update and select
        self.jewelry.size = enums.SizeEnum.XS
        self.personal_item1.type = enums.PersonalItemType.PASSPORT
        self.personal_item2.color = enums.ColorEnum.BLACK
        insert_update_item(self.jewelry)
        insert_update_item(self.personal_item1)
        insert_update_item(self.personal_item2)
        selected = select_items("test@test.com")
        self.assertCountEqual(selected, [self.jewelry, self.personal_item1, self.personal_item2])

        # Delete and select
        delete_item(self.personal_item1)
        delete_item(self.personal_item2)
        delete_item(self.jewelry)
        selected = select_items("test@test.com")
        self.assertCountEqual(selected, [])

        # Delete exceptions
        with self.assertRaises(Exception) as context:
            delete_item(None)
        self.assertEqual(str(context.exception), "delete_item parameter must not be None!")
        with self.assertRaises(Exception) as context:
            delete_item(5)
        self.assertEqual(str(context.exception), "delete_item parameter must be of type Model!")

if __name__ == "__main__":
    unittest.main()