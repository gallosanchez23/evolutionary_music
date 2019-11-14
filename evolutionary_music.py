import numpy as np
from audio_comparer import correlate
from pydub import AudioSegment

from jmetal.core.problem import IntegerProblem
from jmetal.core.solution import IntegerSolution
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
from jmetal.operator import SBXCrossover, PolynomialMutation, BestSolutionSelection
from jmetal.lab.visualization import Plot, InteractivePlot
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.observer import ProgressBarObserver, VisualizerObserver

# folder = 'half_notes'

# e6 = AudioSegment.from_wav(f'data/{folder}/E6.wav')
# s = AudioSegment.from_wav(f'data/{folder}/S.wav')
# c6 = AudioSegment.from_wav(f'data/{folder}/C6.wav')
# d6 = AudioSegment.from_wav(f'data/{folder}/D6.wav')
# g6 = AudioSegment.from_wav(f'data/{folder}/G6.wav')

# combined = e6  + e6  + e6 + (s * 3) + e6  + e6  + e6 + (s * 3) + e6  + g6  + c6  + d6  + e6

# combined.export('data/conc.wav', format='wav')

# correlate('data/conc.wav', 'data/songs/jingle.wav')

NOTES = [
    'A2', 'A3', 'A4', 'A5', 'A6', 'A7',
    'B2', 'B3', 'B4', 'B5', 'B6', 'B7',
    'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
    'D2', 'D3', 'D4', 'D5', 'D6', 'D7',
    'E2', 'E3', 'E4', 'E5', 'E6', 'E7',
    'F2', 'F3', 'F4', 'F5', 'F6', 'F7',
    'G2', 'G3', 'G4', 'G5', 'G6', 'G7',
    'S'
] # List with all note names

class MusicProblem(IntegerProblem):
    def __init__(self):
        self.lower_bound = [0 for i in range(14)]
        self.upper_bound = [41 for i in range(14)]
        self.number_of_variables = 14
        self.number_of_objectives = 1
        self.number_of_constraints = 0
        self.directions = [self.MAXIMIZE]
        self.labels = ['similarity']

    def evaluate(self, solution: IntegerSolution) -> IntegerSolution:
        global NOTES
        combined = AudioSegment.empty()
        for var in solution.variables:
            note = AudioSegment.from_wav(f'data/half_notes/{NOTES[int(var)]}.wav')
            combined += note
        combined.export('data/conc.wav', format='wav')

        solution.objectives[0] = correlate('data/conc.wav', 'data/songs/jingle.wav')

        return solution

    def create_solution(self) -> IntegerSolution:
        solution = IntegerSolution(
            self.lower_bound,
            self.upper_bound,
            self.number_of_objectives,
            self.number_of_constraints
        )
        solution.variables = [np.random.choice(self.upper_bound[0]) for i in range(self.number_of_variables)]
        return solution

    def get_name(self):
        return 'ZDT4'


problem = MusicProblem()
algorithm = GeneticAlgorithm(
    problem=problem,
    offspring_population_size=100,
    mutation=PolynomialMutation(probability=1.0/problem.number_of_variables, distribution_index=20),
    crossover=SBXCrossover(probability=1.0, distribution_index=20),
    termination_criterion=StoppingByEvaluations(max=1000),
    population_size=100,
    selection=BestSolutionSelection()
)

# Used to initialize the algorithm progress bar
algorithm.observable.register(observer=ProgressBarObserver(max=1000))

# Run the algorithm and set the result
algorithm.run()
front = algorithm.get_result()
# front.sort(key=lambda key: key.objectives[0])
print(front)
for i in front.variables:
    print(i)
print(front.objectives[0])