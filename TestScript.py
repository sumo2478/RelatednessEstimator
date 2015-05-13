from Estimator import Estimator
import numpy as np
import scipy.stats as stat
from copy import copy, deepcopy

def main():
	x = Estimator("data/simplified_data.phased", 'data/relationship_mapping', 'CEU')
	genotypes = x.genotypes
	print(np.corrcoef(genotypes[0]['child'], genotypes[18]['parent2']))

	# x.parseRelationshipMapping('data/relationship_mapping', 'CEU')
	# x.constructParentGenotypeMapping('data/simplified_data.phased')

if __name__ == '__main__':
	main()