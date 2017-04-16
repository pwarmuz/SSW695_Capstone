import unittest
import app


class TestISBN(unittest.TestCase):
    def test_isbn10_checksum(self):
        self.assertEqual(app.books.tools.isbn10_checksum("111853971"), '0')


if __name__ == '__main__':
    unittest.main()
