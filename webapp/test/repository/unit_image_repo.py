import unittest
import os
from webapp.repository.image_repo import *

class TestImageRepo(unittest.TestCase):

    # Represents a 20x20 pixel png, top-left red, top-right blue, bottom-left gree, bottom-right yellow
    TEST_PNG_BYTES = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x02\x00\x00\x00\x02\xeb\x8aZ\x00\x00\x00'IDATx\x9cc\xfc\xcf\x80\x0f02\xe0\x93g\xc2\xab\x97\x00\x18\xd5<24\xe3OB\xf8%\x87\xaa\x9fG5\xd3S3\x00b \x04$\x08\x006I\x00\x00\x00\x00IEND\xaeB`\x82"
    # Same thing, but a pink bottem-right instead of yellow
    UPDATED_PNG_BYTES = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x14\x00\x00\x00\x14\x08\x02\x00\x00\x00\x02\xeb\x8aZ\x00\x00\x00)IDATx\x9cc\xfc\xcf\x80\x0f02\xe0\x93g\xc2\xab\x97\x00\x18\xd5<24\xe3OB\x0c\xff\xb3\xb6\xd0\xca\xe6Q\xcd#C3\x00\xe7F\x05B\x1f\x9b\xc4s\x00\x00\x00\x00IEND\xaeB`\x82"

    def setUp(self):
        with open("/webapp/webapp/test/results/test.png", "wb") as f:
            f.write(self.TEST_PNG_BYTES)

    def tearDown(self):
        os.remove("/webapp/webapp/test/results/test.png")
        try:
            os.remove("/webapp/webapp/test/results/test2.png")
        except:
            pass

    def test_get_image(self):
        result = get_image("test.png")
        self.assertEqual(result, self.TEST_PNG_BYTES)

    def test_save_image(self):
        save_image("test2.png", self.UPDATED_PNG_BYTES)

        with open("/webapp/webapp/test/results/test2.png", "rb") as f:
            result = f.read()
        self.assertEqual(result, self.UPDATED_PNG_BYTES)

    def test_update_image(self):
        update_image("test.png", self.UPDATED_PNG_BYTES)

        with open("/webapp/webapp/test/results/test.png", "rb") as f:
            result = f.read()
        self.assertEqual(result, self.UPDATED_PNG_BYTES)

    def delete_update_image(self):
        delete_image("test.png")
        result = os.path.exists("/webapp/webapp/test/results/test.png")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()