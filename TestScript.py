from Estimator import Estimator

def main():
	x = Estimator("data/simplified_data.phased", 'data/relationship_mapping', 'CEU')
	# x.parseRelationshipMapping('data/relationship_mapping', 'CEU')
	x.constructParentGenotypeMapping('data/simplified_data.phased')

if __name__ == '__main__':
	main()