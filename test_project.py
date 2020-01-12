import unittest
from Functions import *

#0.first_name,1.last_name,2.username,3.password,4.entrance,5.total,6.role,7.isInside

class Testusers(unittest.TestCase):
    def test_user(self):
        result = recognize("guyco","456")
        for i in result:
            self.assertEqual(i[0],'Guy')
            self.assertEqual(i[1],'Cohen')
            
    def test_name_do_not_include_numbers(self):
        result=recognize("yona","123")
        for i in result:
            for j in range(0,len(i[3])):
                self.assertGreater(i[0][j],'9')
                
    def test_isInside_valid(self):
        result=recognize("zada","789")
        flag=False
        for i in result:
            if(i[7]=='yes' or i[7]=='no'):
                flag=True
        self.assertTrue(flag)

    def test_is_name_starts_with_big_letter(self):
        result=recognize("tzahi","164")
        for i in result:
            self.assertGreaterEqual(i[0][0],'A')

    def test_is_role_legal(self):
        result=recognize("yonatan","12")
        flag=False
        for i in result:
            if (i[6]=="admin"):
                flag=True
        self.assertEqual(flag,True)    
    
    def test_is_faceRecdUser_is_in_db(self):
        result=face_recognize("guyc")
        self.assertTrue(result)

    def test_TimeFixer_get_numberAsString(self):
        result=Time_Fixer("15.30")
        self.assertIsNotNone(result)

 
if __name__ == '__main__':
    unittest.main()