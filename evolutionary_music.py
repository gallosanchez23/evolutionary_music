import numpy as np
from audio_comparer import correlate
from pydub import AudioSegment

from jmetal.core.problem import BinaryProblem
from jmetal.core.solution import BinarySolution
from jmetal.algorithm.multiobjective.nsgaii import NSGAII
from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
from jmetal.algorithm.singleobjective.evolution_strategy import EvolutionStrategy
from jmetal.operator import SBXCrossover, PolynomialMutation, BestSolutionSelection, SPXCrossover, BinaryTournamentSelection, BinaryTournament2Selection
from jmetal.lab.visualization import Plot, InteractivePlot
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.util.observer import ProgressBarObserver, VisualizerObserver, PrintObjectivesObserver
from jmetal.operator import BitFlipMutation
from jmetal.core.quality_indicator import FitnessValue
from jmetal.util.termination_criterion import StoppingByQualityIndicator

source_audio = AudioSegment.from_file('data/songs/jingle.wav')
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

AUDIO_NOTES = []

def initialize_notes():
    global NOTES, AUDIO_NOTES
    i = 0
    for note in NOTES:
        AUDIO_NOTES.append(AudioSegment.from_wav(f'data/half_notes/{NOTES[i]}.wav'))
        i+=1

def construct_audio_solution(front: BinarySolution):
    global AUDIO_NOTES, source_audio
    combined = AudioSegment.empty()
    for var in front.variables[0]:
        combined += AUDIO_NOTES[var]
    combined.export('data/conc.wav', format='wav')

class MusicProblem(BinaryProblem):
    def __init__(self, number_of_bits: int):
        self.upper_bound = 41 # The number of notes
        self.number_of_bits = number_of_bits
        self.number_of_variables = 1
        self.number_of_objectives = 1
        self.number_of_constraints = 0
        self.obj_directions = [self.MAXIMIZE]
        self.obj_labels = ['similarity']

    def evaluate(self, solution: BinarySolution) -> BinarySolution:
        global AUDIO_NOTES, source_audio
        combined = AudioSegment.empty()
        for var in solution.variables[0]:
            combined += AUDIO_NOTES[var]
        combined.export('data/conc.wav', format='wav')

        solution.objectives[0] = -1 * correlate('data/conc.wav', 'data/songs/jingle.wav')

        return solution

    def create_solution(self) -> BinarySolution:
        solution = BinarySolution(
            number_of_variables=1,
            number_of_objectives=1
        )
        solution.variables[0] = np.random.choice(self.upper_bound, size=self.number_of_bits)
        return solution

    def get_name(self):
        return 'ZDT4'

initialize_notes()

problem = MusicProblem(number_of_bits=12)
algorithm = GeneticAlgorithm(
    problem=problem,
    offspring_population_size=100,
    mutation=BitFlipMutation(probability=1.0/problem.number_of_bits),
    crossover=SPXCrossover(1.0),
    termination_criterion=StoppingByEvaluations(max=5000),
    population_size=100,
    selection=BinaryTournamentSelection()
)

# Used to initialize the algorithm progress bar
algorithm.observable.register(observer=PrintObjectivesObserver())

# Run the algorithm and set the result
algorithm.run()
front = algorithm.get_result()

construct_audio_solution(front)

print(front)
for i in front.variables:
    print(i)
print(front.objectives[0])