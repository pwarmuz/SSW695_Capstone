import unittest
import app


class TestISBN(unittest.TestCase):
    def test_isbn10_checksum(self):
        self.assertEqual(app.books.tools.isbn10_checksum("1118539710"), '0')

    def test_isbn13_checksum(self):
        self.assertEqual(app.books.tools.isbn13_checksum("9781940352602"), '2')

    def test_isbn13_to_isbn10(self):
        self.assertEqual(app.books.tools.isbn13_to_isbn10("9781940352602"), '1940352606')

    def test_isbn10_to_isbn13(self):
        self.assertEqual(app.books.tools.isbn10_to_isbn13("1940352606"), '9781940352602')

    def test_is_isbn(self):
        self.assertEqual(app.books.tools.is_isbn("1937785491"), True)

    def test_is_isbn13(self):
        self.assertEqual(app.books.tools.is_isbn13("9781940352602"), True)

    def test_is_isbn10(self):
        self.assertEqual(app.books.tools.is_isbn10("1118539710"), True)

    def test_validate_isbn13(self):
        self.assertEqual(app.books.tools.validate_isbn13("9781940352602"), None)

    def test_validate_isbn10(self):
        self.assertEqual(app.books.tools.validate_isbn10("1118539710"), None)

if __name__ == '__main__':
    unittest.main()
