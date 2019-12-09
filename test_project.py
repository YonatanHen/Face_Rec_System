import unittest
import entrance



class Testusers(unittest.TestCase):
    def test_recognize(self):
        result = entrance.recognize("guyco","456")
        self.assertEqual(result,True)

    def test_recognize(self):
        result = entrance.recognize("dani","254")
        self.assertEqual(result,False)

if __name__ == '__main__':
    unittest.main()