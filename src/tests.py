import unittest
import app.book.tools


class TestISBN(unittest.TestCase):
    def test_isbn10_checksum(self):
        self.assertEqual(app.book.tools.isbn10_checksum("111853971"), '0')


if __name__ == '__main__':
    unittest.main()
