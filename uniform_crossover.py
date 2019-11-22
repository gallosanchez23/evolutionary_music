import copy
import random
from typing import List
from scipy._lib._util import check_random_state

from jmetal.core.operator import Crossover
from jmetal.core.solution import BinarySolution

class UniformCrossover(Crossover[BinarySolution, BinarySolution]):

	def __init__(self, probability: float):
		super(UniformCrossover, self).__init__(probability = probability)

	def execute(self, parents: List[BinarySolution]) -> List[BinarySolution]:
		# validate precense of only two parents
		if len(parents) != 2:
			raise Exception('The number of parents is not two: {}'.format(len(parents)))

		# create offspring
		offspring = [copy.deepcopy(parents[0]), copy.deepcopy(parents[1])]
		# create mask
		rng = check_random_state(None)
		mask = rng.choice(
			[False, True],
			p = [self.probability, 1 - self.probability],
			size = len(offspring[0].variables[0])
		)

		rand = random.random()
		if rand <= self.probability:
			for i in range(len(mask)):
				# swap elements if the mask element is true
				if mask[i]:
					swap = offspring[0].variables[0][i]
					offspring[0].variables[0][i] = offspring[1].variables[0][i]
					offspring[1].variables[0][i] = swap

		return offspring

	def get_number_of_parents(self) -> int:
		return 2

	def get_number_of_children(self) -> int:
		return 2

	def get_name(self) -> str:
		return 'Uniform crossover'
