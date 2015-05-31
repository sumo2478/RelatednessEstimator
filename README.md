# RelatednessEstimator
The relatedness estimator determines the relatedness of two individuals given two strands of DNA sequences

##Estimator Class
Class that handles the parsing of the hap map data and determining of relatedness

```
e = Estimator(dataFileName, relationshipFileName, region, alleleRelevancyThreshold)
e.determineRelatedness(person1Id, person2Id)
```

## Test Script
Script that provides a simple interface to use to determine relatedness
* Use default estimator? Type y to use basic or n to customize it
* Genotype data file name? The name of the genotype data you want to use
* Relationship file name? The file you want to use for the relationship mapping
* Region to examine? The population you want to examine (CEU, ASW, ...)
* Maximum percent similarity? MAF to use as threshold

Options:
1. Print relationships - Prints the relationship mappings and ID's of people
2. Determine correlation  - Determines correlation between two people given their ID's
3. Determine relatedness of two people - Says whether or not the two people are related

## Sibling Simulator
Simulator that runs multiple tests given parameters and outputs the accuracies given those parameters
