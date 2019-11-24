import random
import numpy as np

from jmetal.core.operator import Mutation
from jmetal.core.solution import BinarySolution

class UniformMutation(Mutation[BinarySolution]):

	def __init__(self, probability: float):
		super(UniformMutation, self).__init__(probability = probability)

	def execute(self, solution: BinarySolution) -> BinarySolution:
		offspring = solution.variables
		popsize = len(solution.variables[0])

		values = np.random.choice(42, popsize)
		probs = np.random.uniform(0, 1, popsize)

		for i in range(popsize):
			if probs[i] <= self.probability:
				offspring[0][i] = values[i]
		
		solution.variables = offspring
		return solution

	def get_name(self):
		return 'Uniform mutation'
