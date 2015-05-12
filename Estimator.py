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
	
	def parseRelationshipMapping(self, fileName, region):
		data = self.readFileIntoMatrix(fileName, 'str')

		# Find rows that correspond to the specified region
		regionMask = data[:, Constants.RELATIONSHIP_REGION_INDEX] == region

		# Determine the indices for the valid entries in the mask
		validEntryIndices = [i for i, x in enumerate(regionMask) if x == True]

		mapping = data[validEntryIndices, :]

		return mapping

	def determineRelatedness(self, sequence1, sequence2):
		return np.corrcoef(sequence1, sequence2)

	def constructParentGenotypeMapping(self, fileName):
		"Creates a mapping of parent Id to genotype A (transmitted) and B (untransmitted)"
		data = self.readFileIntoMatrix(fileName, 'str')

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

	# Helper Functions
	def printFileName(self):
		return self.dataFileName

	def readFileIntoMatrix(self, fileName, type):
		data = np.genfromtxt(fileName, dtype=type)		
		return data