import unittest
from webapp.models.models import *
from webapp.models.enums import *
from webapp.repository.item_repo import *
from webapp.service.account_service import create_user

class TestItemRepo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        create_user("test@test.com", "password", RoleEnum.USER, 12345, "name", "surname")
        cls.personal_item1 = PersonalItems(
            type=PersonalItemType.KEYS,
            color=ColorEnum.GRAY,
            description="My keys",
            status=StatusEnum.LOST,
            email="test@test.com"
        )
        cls.personal_item2 = PersonalItems(
            type=PersonalItemType.CREDIT_DEBIT_CARD,
            color=ColorEnum.WHITE,
            description="My credit card",
            status=StatusEnum.LOST,
            email="test@test.com"
        )
        cls.jewelry = Jewelry(
            type=JewelryType.NECKLACE,
            color=ColorEnum.RED,
            size=SizeEnum.S,
            description="My necklace",
            status=StatusEnum.LOST,
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
        selected = select_item_by_id(self.jewelry.id, Jewelry)
        self.assertEqual(selected, self.jewelry)
        selected = select_item_by_id(self.jewelry.id, TravelItems)
        self.assertEqual(selected, None)

        # Select by id, email exceptions
        with self.assertRaises(Exception) as context:
            select_item_by_id(None, Jewelry)
        self.assertEqual(str(context.exception), "select_item_by_id id must not be None!")
        with self.assertRaises(Exception) as context:
            select_item_by_id("None", Jewelry)
        self.assertEqual(str(context.exception), "select_item_by_id id must be of type int!")

        # Update and select
        self.jewelry.size = SizeEnum.XS
        self.personal_item1.type = PersonalItemType.PASSPORT
        self.personal_item2.color = ColorEnum.BLACK
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