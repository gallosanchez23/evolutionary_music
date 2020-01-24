from pydub import AudioSegment
from music_problem import MusicProblem
from notes_directory import NotesDirectory

from jmetal.operator import SPXCrossover, BinaryTournamentSelection, BitFlipMutation
from jmetal.util.observer import ProgressBarObserver, PrintObjectivesObserver
from jmetal.util.termination_criterion import StoppingByEvaluations
from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm

from uniform_crossover import UniformCrossover
from uniform_mutation import UniformMutation

def generate_audio_file(notes):
	notes_directory = NotesDirectory()

	combined = AudioSegment.empty()
	for var in notes:
		combined += notes_directory.get_audio_note(var)
	combined.export('data/conc.wav', format = 'wav')


target_file = 'data/songs/ode_to_joy.wav'
number_of_notes = 15
problem = MusicProblem(target_file, number_of_notes)
population_size = 100
max_evaluations = 3000

algorithm = GeneticAlgorithm(
	problem = problem,
	mutation = UniformMutation(probability = 1.0 / problem.number_of_notes),
	crossover = UniformCrossover(1.0),
	selection = BinaryTournamentSelection(),
	population_size = population_size,
	termination_criterion = StoppingByEvaluations(max = max_evaluations),
	offspring_population_size = population_size
)

# Initialize progress bar observer
algorithm.observable.register(observer = PrintObjectivesObserver())

# Run algorithm and set results
algorithm.run()
front = algorithm.get_result()

# Create audio file from the best result
generate_audio_file(front.variables[0])
print(front)
