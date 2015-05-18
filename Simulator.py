from Estimator import Estimator

def main():
	e = Estimator('data/large.phased', 'data/relationship_mapping')	
	e.configure('CEU', 0.6)
	# e = Estimator('data/yri_chromosome1.phased', 'data/relationship_mapping')
	# e.configure('YRI', 0.6)

	relationshipMapping = e.relationshipMapping

	correctResults = 0
	totalResults = 0
	print('Computing relationships...')
	for index, relationship in enumerate(relationshipMapping):				
		child = relationship['child']
		parent1 = relationship['parent1']
		parent2 = relationship['parent2']

		try:
			# Compare child with parent1
			relatedCP1 = e.areRelated(child, parent1)
			if relatedCP1:
				correctResults = correctResults + 1
			else:
				print('Incorrect: ' + child + ' with ' + parent1)
			totalResults = totalResults + 1
		except Exception, exc:
			pass		

		# Compare child with parent 2
		try:
			relatedCP2 = e.areRelated(child, parent2)
			if relatedCP2:
				correctResults = correctResults + 1
			else:
				print('Incorrect: ' + child + ' with ' + parent2)
			totalResults = totalResults + 1
		except Exception, exc:
			pass		

		# Compare with the rest of the relations
		for other in relationshipMapping[index+1:]:
			# Compare child with other relations			
			(addedResults, addedTotal) = compareWithOtherRelationFalse(child, other, e) 
			correctResults = correctResults + addedResults
			totalResults = totalResults + addedTotal
			
			# Compare parent1 with other relations
			(addedResults, addedTotal) = compareWithOtherRelationFalse(parent1, other, e)
			correctResults = correctResults + addedResults
			totalResults = totalResults + addedTotal

			# Compare parent2 with other relations
			(addedResults, addedTotal) = compareWithOtherRelationFalse(parent2, other, e)
			correctResults = correctResults + addedResults
			totalResults = totalResults + addedTotal
	
	print('\n====================================================')	
	print('Accuracy: ' + str(correctResults / float(totalResults)))	
	print('====================================================')						

def compareWithOtherRelationFalse(person, other, e):
	correctResults = 0
	totalResults = 0

	otherChild = other['child']
	otherParent1 = other['parent1']
	otherParent2 = other['parent2']

	try:
		related = e.areRelated(person, otherChild)
		if not related:
			correctResults = correctResults + 1
		else:
			print('Incorrect: ' + person + ' with ' + otherChild)
		totalResults = totalResults + 1
	except Exception, exc:
		pass
	
	
	try:
		related = e.areRelated(person, otherParent1)
		if not related:
			correctResults = correctResults + 1
		else:
			print('Incorrect: ' + person + ' with ' + otherParent1)
		totalResults = totalResults + 1
	except Exception, exc:
		pass

	try:
		related = e.areRelated(person, otherParent2)
		if not related:
			correctResults = correctResults + 1
		else:
			print('Incorrect: ' + person + ' with ' + otherParent2)
		totalResults = totalResults + 1
	except Exception, exc:
		pass
	
	return (correctResults, totalResults)


if __name__ == '__main__':
	main()