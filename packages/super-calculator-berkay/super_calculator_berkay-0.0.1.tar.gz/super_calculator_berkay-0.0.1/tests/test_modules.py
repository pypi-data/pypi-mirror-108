import sys, os 
import unittest


testdir = os.path.dirname(__file__)
srcdir = '../super_calculator_banbar'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))


from add_subtract import *
from multiply_divide import *

class TestFunctions(unittest.TestCase):
   
    def setUp(self):        
        # Polygon 1: Simple square - CCW - total must be 360               
        self.num1 = 50
        self.num2 = 5
        self.num3 = 8
    
    def test_add(self):
        self.assertEqual(add_two_numbers(self.num1, self.num2),55)
    
    def test_divide(self):
        self.assertEqual(divide_two_numbers(self.num1, self.num2),10)
        self.assertEqual(divide_two_numbers(self.num1, self.num3),6)
        

if __name__ == '__main__':
    unittest.main()