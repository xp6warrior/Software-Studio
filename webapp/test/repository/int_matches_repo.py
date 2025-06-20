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

    # select_matches_by_item
    def test_select_matches_by_item_success_none(self):
        with rx.session() as session:
            session.add_all([self.account, self.item1, self.item2])
            session.commit()
            session.refresh(self.item1)
            session.refresh(self.item2)
            
        expected_result = []
        result = select_matches_by_item(self.item1)
        self.assertEqual(expected_result, result)

        expected_result = []
        result = select_matches_by_item(self.item2)
        self.assertEqual(expected_result, result)

    def test_select_matches_by_item_success_many(self):
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
        result = select_matches_by_item(self.item1)
        self.assertCountEqual(expected_result, result)

        expected_result = [matcha]
        result = select_matches_by_item(self.item2)
        self.assertCountEqual(expected_result, result)

    def test_select_matches_by_item_fail_param(self):
        with self.assertRaises(Exception) as context:
            select_matches_by_item(None)
        self.assertEqual(str(context.exception), "item must not be None!")

        with self.assertRaises(Exception) as context:
            select_matches_by_item(1234)
        self.assertEqual(str(context.exception), "item must be of type Items!")

    def test_select_match_by_id_success_one(self):
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

        expected_result = matcha
        result = select_match_by_id(matcha.id)
        self.assertEqual(expected_result, result)

    def test_select_match_by_id_success_none(self):
        result = select_match_by_id(5)
        self.assertIsNone(result)

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