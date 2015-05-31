from Estimator import Estimator
import timeit

# def performSimulation(numberOfSnps):
def performSimulation(numberOfSnps):
	print("Examining: " + str(numberOfSnps))
	e = Estimator('data/yri_chromosome1.phased', 'data/relationship_mapping')
	e.configure('YRI', 0.6, numberOfSnps)

	# e = Estimator('data/yri_chromosome1.phased', 'data/relationship_mapping')
	# e.configure('YRI', 0.6)

	relationshipMapping = e.relationshipMapping

	correctResults = 0
	totalResults = 0
	correctSiblingsIdentified = 0
	totalSiblings = 0
	correctNotRelated = 0
	totalNotRelated = 0
	print('Computing relationships...')
	for index, relationship in enumerate(relationshipMapping[1:]):				
		child = relationship['child']
		child2 = relationship['child2']
		parent1 = relationship['parent1']
		parent2 = relationship['parent2']

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldBeRelated(child, child2, e)
		correctSiblingsIdentified = correctSiblingsIdentified + addedCorrect
		totalSiblings = totalSiblings + addedTotal

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldBeRelated(child, parent1, e)
		correctSiblingsIdentified = correctSiblingsIdentified + addedCorrect
		totalSiblings = totalSiblings + addedTotal

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldBeRelated(child2, parent2, e)
		correctSiblingsIdentified = correctSiblingsIdentified + addedCorrect
		totalSiblings = totalSiblings + addedTotal

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldBeRelated(child, parent2, e)
		correctSiblingsIdentified = correctSiblingsIdentified + addedCorrect
		totalSiblings = totalSiblings + addedTotal

		other = relationshipMapping[index-1]
		otherChild = other['child']
		otherParent1 = other['parent1']
		otherParent2 = other['parent2']

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldNotBeRelated(child, otherChild, e)
		correctNotRelated = correctNotRelated + addedCorrect
		totalNotRelated = totalNotRelated + addedTotal		

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldNotBeRelated(child2, otherChild, e)
		correctNotRelated = correctNotRelated + addedCorrect
		totalNotRelated = totalNotRelated + addedTotal

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldNotBeRelated(child, otherParent1, e)
		correctNotRelated = correctNotRelated + addedCorrect
		totalNotRelated = totalNotRelated + addedTotal

		(addedCorrect, addedTotal) = compareWithOtherRelationShouldNotBeRelated(child2, otherParent2, e)
		correctNotRelated = correctNotRelated + addedCorrect
		totalNotRelated = totalNotRelated + addedTotal

		correctResults = correctSiblingsIdentified + correctNotRelated
		totalResults = totalSiblings + totalNotRelated

	relatedAccuracy = correctSiblingsIdentified / float(totalSiblings)
	unrelatedAccuracy = correctNotRelated / float(totalNotRelated)
	totalAccuracy = correctResults / float(totalResults)

	return (relatedAccuracy, unrelatedAccuracy, totalAccuracy)	

def computeTime():
	print("Time: " + str(timeit.timeit(performSimulation, number=10)/10))

def computeAccuracy():
	results = []
	for i in range(1):
		# numberOfSnps = (i+1) * 1000
		numberOfSnps = 500

		rAccuracy = 0
		uAccuracy = 0
		tAccuracy = 0
		n = 10
		for i in range(n):		
			(relatedAccuracy, unrelatedAccuracy, totalAccuracy) = performSimulation(numberOfSnps)
			rAccuracy = rAccuracy + relatedAccuracy
			uAccuracy = uAccuracy + unrelatedAccuracy
			tAccuracy = tAccuracy + totalAccuracy

		rAccuracy = rAccuracy / n
		uAccuracy = uAccuracy / n
		tAccuracy = tAccuracy / n

		# results.append("Num: " + str(numberOfSnps) + "\tRelated Accuracy: " + str(rAccuracy) + "\tUnRelatedAccuracy: " + str(uAccuracy) + "\tTotalAccuracy: " + str(tAccuracy))
		results.append("Total Accuracy: " + str(tAccuracy))
	
	for result in results:
		print(result)		

def main():
	# computeTime()
	computeAccuracy()

def compareWithOtherRelationShouldBeRelated(person1, person2, e):
	correctResults = 0
	totalResults = 0

	try:
		related = e.areRelated(person1, person2)
		if related:
			correctResults = correctResults + 1
		else:
			# print('Incorrect: ' + person1 + ' should be related to ' + person2)
			pass
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
			# print('Incorrect: ' + person1 + ' should not be related to ' + person2)
			pass
		totalResults = totalResults + 1
	except Exception, exc:
		pass	
	
	return (correctResults, totalResults)

if __name__ == '__main__':
	main()
