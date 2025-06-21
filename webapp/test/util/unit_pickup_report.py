import unittest
from webapp.util.pickup_report import generate_pickup_report

class TestPickupReport(unittest.TestCase):

    def test_generate_pickup_report(self):
        owner_details = {
            "name": "name",
            "surname": "surname",
            "email": "test@domain.com",
            "pesel": "12345678910"
        }
        item_details = {
            "id": "5",
            "category": "personal_item",
            "type": "passport",
            "size": "m",
            "color": "red",
            "description": "Polish passport"
        }

        result = generate_pickup_report(owner_details, item_details)
        with open("/webapp/webapp/test/results/test.pdf", 'wb') as f:
            f.write(result)

if __name__ == "__main__":
    unittest.main()