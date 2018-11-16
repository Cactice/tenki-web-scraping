import unittest
from tenki_web_scraping import get_climate



class TestMethods(unittest.TestCase):
    def test_get_climate(self):
        expected = ['はれ', '雨', '13.4', '8.4']
        actual = get_climate('香川県','151216')
        self.assertSequenceEqual(expected,actual)

if __name__ == '__main__':
    unittest.main()

