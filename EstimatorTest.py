import unittest
from Estimator import Estimator

class TestRelatednessEstimation(unittest.TestCase):
	def test_determine_relatedness(self):
		x = Estimator("file")
		self.assertEqual(x.printFileName(), "file")

if __name__ == '__main__':
	unittest.main()