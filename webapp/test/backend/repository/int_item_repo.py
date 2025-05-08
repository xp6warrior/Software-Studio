import unittest
import webapp.models.models as models
import webapp.models.enums as enums
from webapp.backend.repository.item_repo import *
from webapp.backend.service.login_service import create_user

class TestSelectItem(unittest.TestCase):
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
        selected = select_items("test@test.com")
        self.assertCountEqual(selected, [jewelry, personal_item, personal_item2])

        # Update and select
        jewelry.size = enums.SizeEnum.XS
        personal_item.type = enums.PersonalItemType.PASSPORT
        personal_item2.color = enums.ColorEnum.BLACK
        insert_update_item(jewelry)
        insert_update_item(personal_item)
        insert_update_item(personal_item2)
        selected = select_items("test@test.com")
        self.assertCountEqual(selected, [jewelry, personal_item, personal_item2])

        # Delete and select
        delete_item(personal_item2)
        selected = select_items("test@test.com")
        self.assertCountEqual(selected, [jewelry, personal_item])

if __name__ == "__main__":
    unittest.main()