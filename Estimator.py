import numpy as np
import scipy.stats as stat
from copy import copy, deepcopy

import Constants

class Estimator():
	"""Relatedness Estimator"""
	def __init__(self, dataFileName, relationshipFileName, region):
		"""
		Initializer for Estimator
		@param {string} dataFileName - The file name for the genotype data
		@param {string} relationshipFileName - The file name for the parent relationships
		@param {string} region - The three character region identifier i.e. CEU
		"""
		self.dataFileName = dataFileName
		self.relationshipFileName = relationshipFileName
		self.region = region
		self.relationshipMapping = self.parseRelationshipMapping(relationshipFileName, region)		
		self.genotypeMapping = self.constructParentGenotypeMapping(dataFileName)
		self.genotypes = self.constructGenotypes(self.relationshipMapping, self.genotypeMapping)
	
	def parseRelationshipMapping(self, fileName, region):
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

		mapping = mapping[validParentEntryIndices, Constants.RELATIONSHIP_PARENT1_ID_INDEX:Constants.RELATIONSHIP_PARENT2_ID_INDEX+1]		
		mapping = [{'parent1': row[0], 'parent2': row[1]} for row in mapping]	
		
		return mapping

	def determineRelatedness(self, sequence1, sequence2):		
		return np.corrcoef(sequence1, sequence2)

	def constructParentGenotypeMapping(self, fileName):
		"Creates a mapping of parent Id to genotype A (transmitted) and B (untransmitted)"
		data = self.readFileIntoMatrix(fileName, 'str')

		nonTrivialIndices = self.indicesOfNonTrivialAlleles(data, 0.9)
		
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
		genotypes = []

		# For each relationship in the relationship mapping
		for relationship in relationshipMapping:
			try:
				# Concatenate the transmitted genotypes for parent 1 and parent 2 to 
				# get the genotypes of the children
				parent1 = genotypeMapping[relationship['parent1']]
				parent2 = genotypeMapping[relationship['parent2']]

				childGenotype = parent1['transmitted'] + parent2['transmitted']
				parent1Genotype = parent1['transmitted'] + parent1['untransmitted']
				parent2Genotype = parent2['transmitted'] + parent2['untransmitted']							

				genotypeEntry = {
					'child': childGenotype,
					'parent1': parent1Genotype,
					'parent2': parent2Genotype
				}

				genotypes.append(genotypeEntry)				
			except KeyError:
				continue
		
		return genotypes

	# Helper Functions
	def printFileName(self):
		return self.dataFileName

	def readFileIntoMatrix(self, fileName, type):
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
			








