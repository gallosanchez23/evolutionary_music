import numpy as np
from pydub import AudioSegment
from notes_directory import NotesDirectory
from audio_comparer_ii import AudioComparer

from jmetal.core.problem import BinaryProblem
from jmetal.core.solution import BinarySolution

class MusicProblem(BinaryProblem):

	def __init__(self, target_name: str, number_of_notes: int):
		self.number_of_notes = number_of_notes
		self.number_of_variables = 1
		self.number_of_objectives = 1
		self.number_of_constraints = 0
		self.number_of_available_notes = 42
		self.obj_labels = ['similarity']
		self.obj_directions = [self.MAXIMIZE]
		self.audio_comparer = AudioComparer()
		self.notes_directory = NotesDirectory()

		self.audio_comparer.set_target(target_name)

	def evaluate(self, solution: BinarySolution) -> BinarySolution:
		combined = AudioSegment.empty()
		for note_index in solution.variables[0]:
			combined += self.notes_directory.get_audio_note(note_index)
		combined.export('data/conc.wav', format='wav')

		solution.objectives[0] = \
			-1 * self.audio_comparer.compare('data/conc.wav')

		return solution

	def create_solution(self) -> BinarySolution:
		solution = BinarySolution(
			self.number_of_variables,
			self.number_of_objectives
		)

		solution.variables[0] = np.random.choice(
			self.number_of_available_notes,
			size = self.number_of_notes
		)

		return solution

	def get_name(self):
		return 'Music problem'
