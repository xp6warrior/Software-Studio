import unittest
import webapp.models.models as models
import webapp.models.enums as enums
from webapp.backend.repository.item_repo import *
from webapp.backend.service.login_service import create_user

class TestItemCrud(unittest.TestCase):
    def test_item_crud_success(self):
        # Setup
        create_user("test@test.com", "password", enums.RoleEnum.USER)
        personal_item = models.PersonalItems(
            type=enums.PersonalItemType.KEYS,
            color=enums.ColorEnum.GRAY,
            description="My keys",
            status=enums.StatusEnum.LOST,
            email="test@test.com"
        )
        personal_item2 = models.PersonalItems(
            type=enums.PersonalItemType.CREDIT_DEBIT_CARD,
            color=enums.ColorEnum.WHITE,
            description="My credit card",
            status=enums.StatusEnum.LOST,
            email="test@test.com"
        )
        jewelry = models.Jewelry(
            type=enums.JewelryType.NECKLACE,
            color=enums.ColorEnum.RED,
            size=enums.SizeEnum.S,
            description="My necklace",
            status=enums.StatusEnum.LOST,
            email="test@test.com"
        )

        # Insert and select
        insert_update_item(jewelry)
        insert_update_item(personal_item)
        insert_update_item(personal_item2)
        selected = select_items_by_email("test@test.com")
        self.assertCountEqual(selected, [jewelry, personal_item, personal_item2])

        # Update and select
        jewelry.size = enums.SizeEnum.XS
        personal_item.type = enums.PersonalItemType.PASSPORT
        personal_item2.color = enums.ColorEnum.BLACK
        insert_update_item(jewelry)
        insert_update_item(personal_item)
        insert_update_item(personal_item2)
        selected = select_items_by_email("test@test.com")
        self.assertCountEqual(selected, [jewelry, personal_item, personal_item2])

        # Delete and select
        delete_item(personal_item2)
        selected = select_items_by_email("test@test.com")
        self.assertCountEqual(selected, [jewelry, personal_item])

        # Select by id and email
        selected = select_item_by_id_email(jewelry.id, "test@test.com", models.Jewelry)
        self.assertEqual(selected, jewelry)

        selected = select_item_by_id_email(jewelry.id, "other@email.com", models.Jewelry)
        self.assertEqual(selected, None)

if __name__ == "__main__":
    unittest.main()