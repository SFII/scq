import unittest

from services.survey import Survey, Surveys

class TestServices(unittest.TestCase):

    def test_silly(self):
        self.assertEqual(pow(2,7,11), 7)

if __name__ == '__main__':
    unittest.main()
