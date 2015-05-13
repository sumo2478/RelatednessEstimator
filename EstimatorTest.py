import unittest
from Estimator import Estimator

import Constants

class TestRelatednessEstimation(unittest.TestCase):
	def test_determine_relatedness(self):
		x = Estimator("data/simplified_data.phased", "data/relationship_mapping", 'CEU')
		self.assertEqual(x.printFileName(), "data/simplified_data.phased")

	def test_reading_relationship_mapping_files(self):
		estimator = Estimator("data/simplified_data.phased", "data/relationship_mapping", 'CEU')
		relationshipMapping = estimator.relationshipMapping
		relationship = relationshipMapping[0]
		self.assertEqual(relationship['parent1'], 'NA12748')
		self.assertEqual(relationship['parent2'], 'NA12749')

	def test_construct_parent_genotype_mapping(self):
		estimator = Estimator("data/simplified_data.phased", "data/relationship_mapping", 'CEU')
		genotypeMapping = estimator.genotypeMapping
		self.assertTrue('NA12144' in genotypeMapping)
		self.assertEqual(genotypeMapping['NA12749']['transmitted'][0], 1)		

if __name__ == '__main__':
	unittest.main()