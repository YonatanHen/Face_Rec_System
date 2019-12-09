import unittest
import entrance

#0.first_name,1.last_name,2.username,3.password,4.entrance,5.total,6.role,7.isInside

class Testusers(unittest.TestCase):
    def test_user(self):
        result = entrance.recognize("guyco","456")
        for i in result:
            self.assertEqual(i[0],'Guy')
            self.assertEqual(i[1],'Cohen')

    def test_name_do_not_include_numbers(self):
        result=entrance.recognize("yona","123")
        for i in result:
            for j in range(0,len(i[3])):
                self.assertGreater(i[0][j],'9')

    def test_isInside_valid(self):
        result=entrance.recognize("zada","789")
        flag=False
        for i in result:
            if(i[7]=='yes' or i[7]=='no'):
                flag=True
            break
        self.assertTrue(flag)
    def is_name_starts_with_big_letter(self):
        result=entrance.recognize("tzahi","164")
        for i in result:
            self.assertGreaterEqual(i[0][0],'A')
 

if __name__ == '__main__':
    unittest.main()