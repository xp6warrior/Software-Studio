import unittest
from webapp.models.models import *
from webapp.models.enums import MatchStatus
from webapp.repository.matches_repo import *

class TestMatchesRepo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.match1 = Match(
            table_name="personalitems",
            lost_item_id=4,
            found_item_id=7,
            status=MatchStatus.UNCONFIRMED,
            percentage=80
        )
        cls.match2 = Match(
            table_name="personalitems",
            lost_item_id=5,
            found_item_id=7,
            status=MatchStatus.CONFIRMED,
            percentage=90
        )
        insert_update_match(cls.match1)
        insert_update_match(cls.match2)

    def test_select_matches(self):
        selected = select_matches(7, PersonalItems)
        self.assertCountEqual(selected, [self.match1, self.match2])

        # Exceptions
        with self.assertRaises(Exception) as context:
            select_matches(None, PersonalItems)
        self.assertEqual(str(context.exception), "select_matches found_id must not be None!")
        
        with self.assertRaises(Exception) as context:
            select_matches("None", PersonalItems)
        self.assertEqual(str(context.exception), "select_matches found_id must be of type int!")

    def test_update_matches(self):
        self.match2.status = MatchStatus.UNCONFIRMED
        insert_update_match(self.match2)

        selected = select_matches(7, PersonalItems)
        self.assertCountEqual(selected, [self.match1, self.match2])