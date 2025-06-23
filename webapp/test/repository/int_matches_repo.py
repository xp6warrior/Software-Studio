import unittest
import reflex as rx
from sqlalchemy import select, delete

from webapp.models2.models import Accounts, PersonalItems, Matches
from webapp.models2.enums import RoleEnum, PersonalItemType, ColorEnum, StatusEnum, MatchStatusEnum
from webapp.repository.matches_repo import *

class TestMatchesRepo(unittest.TestCase):

    def setUp(self):
        self.account = Accounts(email='test.com', name='name', surname='surname', role=RoleEnum.USER, password='pass')
        self.item1 = PersonalItems(status=StatusEnum.LOST, email='test.com', type=PersonalItemType.PASSPORT, color=ColorEnum.RED)
        self.item2 = PersonalItems(status=StatusEnum.FOUND, email='test.com', type=PersonalItemType.PASSPORT, color=ColorEnum.RED)
    
    def tearDown(self):
        with rx.session() as session:
            session.exec(delete(Accounts))
            session.exec(delete(Items))
            session.exec(delete(Matches))
            session.commit()

    # select_matches
    def test_select_matches_success_none(self):
        with rx.session() as session:
            session.add_all([self.account, self.item1, self.item2])
            session.commit()
            session.refresh(self.item1)
            session.refresh(self.item2)
            
        expected_result = []
        result = select_matches(self.item1)
        self.assertEqual(expected_result, result)

        expected_result = []
        result = select_matches(self.item2)
        self.assertEqual(expected_result, result)

    def test_select_matches_success_many(self):
        with rx.session() as session:
            session.add_all([self.account, self.item1, self.item2])
            session.commit()
            matcha = Matches(status=MatchStatusEnum.UNCONFIRMED, percentage=100, 
                                lost_item_id=self.item1.id, found_item_id=self.item2.id)
            session.add(matcha)
            session.commit()
            session.refresh(self.item1)
            session.refresh(self.item2)
            session.refresh(matcha)

        expected_result = [matcha]
        result = select_matches(self.item1, 0, 1)
        self.assertCountEqual(expected_result, result)

        expected_result = [matcha]
        result = select_matches(self.item2, 0, 1)
        self.assertCountEqual(expected_result, result)

    def test_select_matches_fail_param(self):
        with self.assertRaises(Exception) as context:
            select_matches(None)
        self.assertEqual(str(context.exception), "item must not be None!")

        with self.assertRaises(Exception) as context:
            select_matches(1234)
        self.assertEqual(str(context.exception), "item must be of type Items!")

        with self.assertRaises(Exception) as context:
            select_matches(self.item1, None, None)
        self.assertEqual(str(context.exception), "offset and limit must not be None!")

        with self.assertRaises(Exception) as context:
            select_matches(self.item1, "134")
        self.assertEqual(str(context.exception), "offset and limit must be of type int!")

        with self.assertRaises(Exception) as context:
            select_matches(self.item1, 4, -2)
        self.assertEqual(str(context.exception), "offset and limit must be at least 0, and in ascending order!")

    # update match
    def test_update_match(self):
        with rx.session() as session:
            session.add_all([self.account, self.item1, self.item2])
            session.commit()
            matcha = Matches(status=MatchStatusEnum.UNCONFIRMED, percentage=100, 
                                lost_item_id=self.item1.id, found_item_id=self.item2.id)
            session.add(matcha)
            session.commit()
            session.refresh(self.item1)
            session.refresh(self.item2)
            session.refresh(matcha)

        matcha.percentage = 80
        insert_update_match(matcha)

        with rx.session() as session:
            result = session.exec(
                select(Matches).where(Matches.id == matcha.id)
            ).scalars().all()

        expected_result = [matcha]
        self.assertCountEqual(expected_result, result)

if __name__ == "__main__":
    unittest.main()