import numpy as np
import scipy.stats as stat
from copy import copy, deepcopy

class Estimator():
	"""Relatedness Estimator"""
	def __init__(self, dataFileName):
		self.dataFileName = dataFileName

	def printFileName(self):
		return self.dataFileName
	
	def determineRelatedness(self, sequence1, sequence2):
		return np.corrcoef(sequence1, sequence2)