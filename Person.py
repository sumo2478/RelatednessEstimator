import Constants

class Person():
	"""Person class"""
	def __init__(self, personId, chr1, chr2, parent1=None, parent2=None):
		self.personId = personId
		self.chr1 = chr1
		self.chr2 = chr2
		self.parent1 = parent1
		self.parent2 = parent2