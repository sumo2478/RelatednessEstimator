from Estimator import Estimator
import numpy as np
import scipy.stats as stat
from copy import copy, deepcopy

def main():
	x = Estimator("data/ceu_chromosome1.phased", 'data/relationship_mapping', 'CEU')
	genotypes = x.genotypes
	
	# print(np.corrcoef(genotypes[7]['child'], genotypes[7]['parent2']))

	# x.parseRelationshipMapping('data/relationship_mapping', 'CEU')
	# x.constructParentGenotypeMapping('data/simplified_data.phased')

if __name__ == '__main__':
	main()