import numpy as np
import scipy.stats as stat
from copy import copy, deepcopy
import itertools

import Constants
from Person import Person

class Estimator():
	"""Relatedness Estimator"""
	def __init__(self, dataFileName, relationshipFileName, region='CEU', alleleRelvancyThreshold=0.75):
		"""
		Initializer for Estimator
		@param {string} dataFileName - The file name for the genotype data
		@param {string} relationshipFileName - The file name for the parent relationships
		@param {string} region - The three character region identifier i.e. CEU
		"""		
		self.dataFileName = dataFileName
		self.relationshipFileName = relationshipFileName
		self.region = None
		self.relationshipMapping = None
		self.genotypeMapping = None
		self.genotypes = None		
		self.numSNPs = None

	def configure(self, region, alleleRelvancyThreshold, numSNPs=None):
		print('Configuring...')
		self.region = region		
		self.numSNPs = numSNPs
		self.relationshipMapping = self.parseRelationshipMapping(self.relationshipFileName, self.region)		
		self.genotypeMapping = self.constructParentGenotypeMapping(self.dataFileName, alleleRelvancyThreshold, numSNPs)
		self.genotypes = self.constructGenotypes(self.relationshipMapping, self.genotypeMapping)		
	
	def parseRelationshipMapping(self, fileName, region):
		print("Creating relationship map...")

		data = self.readFileIntoMatrix(fileName, 'str')

		# Find rows that correspond to the specified region
		regionMask = data[:, Constants.RELATIONSHIP_REGION_INDEX] == region
		
		# Determine the indices for the valid entries in the mask
		validEntryIndices = [i for i, x in enumerate(regionMask) if x == True]

		mapping = data[validEntryIndices, :]

		# Remove entries that don't have two parents
		parent1Mask = mapping[:, Constants.RELATIONSHIP_PARENT1_ID_INDEX] != '0'
		parent2Mask = mapping[:, Constants.RELATIONSHIP_PARENT2_ID_INDEX] != '0'
		
		validParentEntryIndices = [i for i, parent1 in enumerate(parent1Mask) if parent1 and parent2Mask[i]]

		mapping = mapping[validParentEntryIndices, Constants.RELATIONSHIP_CHILD_ID_INDEX:Constants.RELATIONSHIP_PARENT2_ID_INDEX+1]		
		mapping = [{'parent1': row[1], 'parent2': row[2], 'child':row[0], 'child2':row[0] + '_2'} for row in mapping]	
		
		return mapping

	def determineRelatedness(self, person1Id, person2Id):
		person1 = self.genotypes[person1Id]
		person2 = self.genotypes[person2Id]

		corrChr1P1Chr1 = np.corrcoef(person1.chr1, person2.chr1)
		corrChr1P1Chr2 = np.corrcoef(person1.chr1, person2.chr2)
		corrChr1P2Chr1 = np.corrcoef(person1.chr2, person2.chr1)
		corrChr1P2Chr2 = np.corrcoef(person1.chr2, person2.chr2)

		totalSum = corrChr1P1Chr1 + corrChr1P1Chr2 + corrChr1P2Chr1 + corrChr1P2Chr2 
		average = totalSum / 4
		
		return average

	def constructParentGenotypeMapping(self, fileName, alleleRelvancyThreshold, numSNPs=None):
		"""
		Creates a mapping of parent Id to genotype A (transmitted) and B (untransmitted)
		- Structure of output:
		{		
			transmitted:   [1 0 0 1 ...]
			untransmitted: [0 0 0 1 ...]
		}
		"""

		print("Constructing parent genotype map...")		

		data = self.readFileIntoMatrix(fileName, 'str', numSNPs)					

		nonTrivialIndices = self.indicesOfNonTrivialAlleles(data, alleleRelvancyThreshold)
		
		data = data[nonTrivialIndices, :]

		genotypeMapping = {}

		for genotype in data[:, 2:].T:
			columnIdentifier = genotype[Constants.CHROMOSOME_PARENT_INDEX]
			personId = columnIdentifier[ : -2] # The id of the person
			geneTransmitted = Constants.TRANSMITTED_MAP[columnIdentifier[-2:]] # Boolean determining whether or not gene was transmitted

			# Retrieve the array of genotypes
			genotypeArray = [Constants.ALLELE_TO_INDEX_MAP[x] for x in genotype[1:]]				

			# Retrieve the person from the genotype mapping
			person = None
			if personId in genotypeMapping:
				person = genotypeMapping[personId]
			else:
				person = {}
				
			# Set the person transmitted alleles
			if geneTransmitted:
				person['transmitted'] = genotypeArray
			else:
				person['untransmitted'] = genotypeArray

			# Set the person back to the position in the genotypeMapping
			genotypeMapping[personId] = person	

		return genotypeMapping	

	def constructGenotypes(self, relationshipMapping, genotypeMapping):
		"""
		Creates a genotyped data
		- Structure of the output:
		{
			parent1: [0 1 0 0 1 ...]
			parent2: [1 0 1 1 0 ...]
			child: [1 1 0 0 1 ...]
		}
		"""
		print("Constructing genotypes and breeding...")

		genotypes = {}

		# For each relationship in the relationship mapping
		for relationship in relationshipMapping:
			try:
				parent1Id = relationship['parent1']
				parent2Id = relationship['parent2']
				childId = relationship['child']

				# Concatenate the transmitted genotypes for parent 1 and parent 2 to 
				# get the genotypes of the children
				parent1 = genotypeMapping[parent1Id]
				parent2 = genotypeMapping[parent2Id]

				childChromosome1 = parent1['transmitted']
				childChromosome2 = parent2['transmitted']
				childPerson = Person(childId, childChromosome1, childChromosome2, parent1, parent2)								

				parent1Person = Person(parent1Id, parent1['transmitted'], parent1['untransmitted'])				

				parent2Person = Person(parent2Id, parent2['transmitted'], parent2['untransmitted'])				

				childPerson2 = self.createChild(parent1Person, parent2Person, childId + '_2')

				genotypes[childPerson.personId] = childPerson
				genotypes[parent1Person.personId] = parent1Person
				genotypes[parent2Person.personId] = parent2Person
				genotypes[childPerson2.personId] = childPerson2
			except KeyError:
				continue
		
		return genotypes

	def createChild(self, parent1, parent2, childId):
		sizeOfGenome = len(parent1.chr1)
		randomSelectionParent1 = np.random.random_integers(0, 1, sizeOfGenome)
		randomSelectionParent2 = np.random.random_integers(0, 1, sizeOfGenome)

		chr1 = []
		chr2 = []

		for i in range(sizeOfGenome):
			selectionParent1 = randomSelectionParent1[i]
			if selectionParent1 == 0:
				chr1.append(parent1.chr1[i])
			else:
				chr1.append(parent1.chr2[i])

			selectionParent2 = randomSelectionParent2[i]
			if selectionParent2 == 0:
				chr2.append(parent2.chr1[i])
			else:
				chr2.append(parent2.chr2[i])

		return Person(childId, chr1, chr2, parent1, parent2)



	def printRelationships(self, amount):
		"""
		Prints the relationships between child, parent1, and parent2
		@param {int} amount - Number of results to display
		"""
		print("====================================================================================")
		print("Relationships::")
		print("====================================================================================")
		for relationship in self.relationshipMapping[:amount]:
			print('Child: ' + relationship['child'] + '		Child2: ' + relationship['child2'] + '		Parent1: ' + relationship['parent1'] + ' 	Parent2: ' + relationship['parent2'])

	def areRelated(self, person1, person2):
		corr = self.determineRelatedness(person1, person2)
		if corr[0, 1] > 0.1:
			return True
		else:
			return False

	# Helper Functions	
	def printFileName(self):
		return self.dataFileName

	def readFileIntoMatrix(self, fileName, type, numToSkip=None):
		data = None
		if numToSkip:			
			t_in = open(fileName)	     		
			data = np.genfromtxt(itertools.islice(t_in, numToSkip), dtype=type)
		else:
			data = np.genfromtxt(fileName, dtype=type)		

		return data

	def indicesOfNonTrivialAlleles(self, genotypeData, percentRelated):
		"""
		Removes the trivial alleles from the data set
		Determines the proportion of alleles and if one is either greater than
		or less than 1-percentRelated then it is removed from the dataset
		"""		
		indicesToReturn = [0]
		totalLength = len(genotypeData[0])
		for index, allele in enumerate(genotypeData[1:, 2:]):
			totalSum = 0

			for entry in allele:
				totalSum = totalSum + Constants.ALLELE_TO_INDEX_MAP[entry]

			ratio = totalSum / float(totalLength)
			if ratio < percentRelated and ratio > (1 - percentRelated):
				indicesToReturn.append(index + 1)

		return indicesToReturn
			








