from Estimator import Estimator

def main():
	e = Estimator('data/ceu_chromosome1.phased', 'data/relationship_mapping')
	e.configure('CEU', 0.6, 20000)

	# e = Estimator('data/yri_chromosome1.phased', 'data/relationship_mapping')
	# e.configure('YRI', 0.6)

	relationshipMapping = e.relationshipMapping

	correctResults = 0
	totalResults = 0
	print('Computing relationships...')
	for index, relationship in enumerate(relationshipMapping[1:]):				
		child = relationship['child']
		child2 = relationship['child2']
		parent1 = relationship['parent1']
		parent2 = relationship['parent2']

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldBeRelated(child, child2, e)
		correctResults = correctResults + addedCorrect
		totalResults = totalResults + addedTotal

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldBeRelated(child, parent1, e)
		correctResults = correctResults + addedCorrect
		totalResults = totalResults + addedTotal

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldBeRelated(child2, parent2, e)
		correctResults = correctResults + addedCorrect
		totalResults = totalResults + addedTotal

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldBeRelated(child, parent2, e)
		correctResults = correctResults + addedCorrect
		totalResults = totalResults + addedTotal

		other = relationshipMapping[index-1]
		otherChild = other['child']
		otherParent1 = other['parent1']
		otherParent2 = other['parent2']

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldNotBeRelated(child, otherChild, e)
		correctResults = correctResults + addedCorrect
		totalResults = totalResults + addedTotal

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldNotBeRelated(child2, otherChild, e)
		correctResults = correctResults + addedCorrect
		totalResults = totalResults + addedTotal

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldNotBeRelated(child, otherParent1, e)
		correctResults = correctResults + addedCorrect
		totalResults = totalResults + addedTotal

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldNotBeRelated(child2, otherParent2, e)
		correctResults = correctResults + addedCorrect
		totalResults = totalResults + addedTotal

	
	print('\n====================================================')	
	print('Accuracy: ' + str(correctResults / float(totalResults)))	
	print('====================================================')						

def compareWithOtherRelationShouldBeRelated(person1, person2, e):
	correctResults = 0
	totalResults = 0

	try:
		related = e.areRelated(person1, person2)
		if related:
			correctResults = correctResults + 1
		else:
			print('Incorrect: ' + person1 + ' should be related to ' + person2)
		totalResults = totalResults + 1
	except Exception, exc:
		pass	
	
	return (correctResults, totalResults)

def compareWithOtherRelationShouldNotBeRelated(person1, person2, e):
	correctResults = 0
	totalResults = 0

	try:
		related = e.areRelated(person1, person2)
		if not related:
			correctResults = correctResults + 1
		else:
			print('Incorrect: ' + person1 + ' should not be related to ' + person2)
		totalResults = totalResults + 1
	except Exception, exc:
		pass	
	
	return (correctResults, totalResults)

if __name__ == '__main__':
	main()