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

		for i in range(popsize):
			indexes = [j for j in range(popsize) if i != j]
			a, b, c = \
				solution.variables[0][np.random.choice(indexes, 3, replace = False)]
			offspring[0][i] = np.clip(a + self.probability * (b - c), 0, 42)

		solution.variables = offspring
		return solution

	def get_name(self):
		return 'Uniform mutation'
