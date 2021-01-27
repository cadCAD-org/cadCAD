import unittest
from parameterized import parameterized, parameterized_class

@parameterized_class(('a', 'b'), [
   (1, 2),
   (5, 5),
])
class TestMathClass(unittest.TestCase):
   def test_add(self):
      self.assertEqual(self.a, self.b)

if __name__ == '__main__':
    unittest.main()