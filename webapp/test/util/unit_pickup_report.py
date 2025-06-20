import unittest
import base64
from webapp.util.pickup_report import generate_pickup_report

class TestPickupReport(unittest.TestCase):

    # TODO make this export pdf into pc rather than into docker container
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

        result = generate_pickup_report("test.pdf", owner_details, item_details)
        
        pdf_data = base64.b64decode(result, validate=True)
        with open("test.pdf", 'wb') as f:
            f.write(pdf_data)

if __name__ == "__main__":
    unittest.main()