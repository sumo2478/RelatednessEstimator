from Estimator import Estimator
import numpy as np
import scipy.stats as stat
from copy import copy, deepcopy

def main():			
	# estimator = Estimator("data/ceu_chromosome1.phased", 'data/relationship_mapping', 'CEU')

	estimator = None
	print('\n')
	print("Welcome to the Relatedness Estimator")

	defaultOption = raw_input('\nUse default estimator? [y/n] ')
	if(defaultOption == 'y'):		
		# estimator = Estimator("data/simplified_data.phased", 'data/relationship_mapping')				
		estimator = Estimator("data/ceu_chromosome1.phased", 'data/relationship_mapping')				
		# estimator = Estimator("data/asw_chromosome1.phased", 'data/relationship_mapping')				
		configureEstimator(estimator)
	else:
		dataFileName = raw_input('Genotype data file name: ')
		relationshipFileName = raw_input('Relationship file name: ')
		estimator = Estimator(dataFileName, relationshipFileName)
		configureEstimator(estimator)

	while True:
		try:			
			print("\nPlease select an option: ")
			print("1: Print relationships")
			print('2: Determine correlation between two people')		
			print('3: Determine relatedness of two people')
			print('4: Configure estimator')
			print('5: Exit')
			input = raw_input()
			
			if (input == '1'):
				printRelationshipOption(estimator)
			elif (input == '2'):
				determineCorrelationOption(estimator)			
			elif(input == '3'):
				determineRelatendessOption(estimator)
			elif (input == '4'):
				configureEstimator(estimator)
			elif (input == '5'):
				return
			else:
				print('Invalid input')
		except Exception, e:
			print('Error: ' + str(e))

def printRelationshipOption(estimator):
	try:
		amount = int(raw_input('Number of results to display: '))
	except Exception, e:
		print('Invalid input defaulting to 10...')
		amount = 10
	
	estimator.printRelationships(amount)

def determineCorrelationOption(estimator):	
	try:
		person1 = raw_input('Id of the first person: ')
		person2 = raw_input('Id of the second person: ')
		corr = estimator.determineRelatedness(person1, person2)
		print('Correlation is: ' + str(corr[0, 1]))
	except Exception, e:
		print('Error: ' + str(e))

def determineRelatendessOption(estimator):
	person1 = raw_input('Id of the first person: ')
	person2 = raw_input('Id of the second person: ')
	corr = estimator.determineRelatedness(person1, person2)
	if corr[0, 1] > 0.1:
		print('\nRelated')
	else:
		print('\nNo relation found')

def configureEstimator(estimator):
	region = raw_input('Region to examine: ')
	alleleRelevancyThreshold = float(raw_input('Maximum percent similarity in alleles: '))

	estimator.configure(region, alleleRelevancyThreshold)

if __name__ == '__main__':
	main()