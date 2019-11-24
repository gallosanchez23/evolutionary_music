import numpy as np
from pydub import AudioSegment
from notes_directory import NotesDirectory
from audio_comparer import AudioComparer

from jmetal.core.problem import BinaryProblem
from jmetal.core.solution import BinarySolution

# Analizing frequencies
from scipy.io import wavfile
import crepe

class MusicProblem(BinaryProblem):

	def __init__(self, target_name: str, number_of_notes: int):
		self.number_of_notes = number_of_notes
		self.number_of_variables = 2
		self.number_of_objectives = 1
		self.number_of_constraints = 0
		self.number_of_available_notes = 42
		self.obj_labels = ['similarity']
		self.obj_directions = [self.MAXIMIZE]
		self.audio_comparer = AudioComparer(target_name)
		self.notes_directory = NotesDirectory()

		self.note_candidates = self.set_frequency_ranges()

	def set_frequency_ranges(self):
		range_constant = 50
		sr, audio = wavfile.read(self.audio_comparer.target_name)

		time, frequency, confidence, activation = crepe.predict(audio, sr, step_size=350)

		candidates = []
		for i in range(self.number_of_notes):
			if i < len(frequency):
				min_freq = max([frequency[i] - range_constant, 0])
				max_freq = frequency[i] + range_constant
				candidate_notes = \
					filter(lambda i: self.notes_directory.NOTE_FREQUENCIES[i] >= min_freq and self.notes_directory.NOTE_FREQUENCIES[i] <= max_freq, range(self.number_of_available_notes))
				candidates.append(list(candidate_notes))
			else:
				candidates.append(list(range(self.number_of_available_notes)))
		return candidates

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

		notes = [np.random.choice(self.note_candidates[i]) for i in range(self.number_of_notes)]
		solution.variables[0] = notes
		solution.variables[1] = self.note_candidates

		return solution

	def get_name(self):
		return 'Music problem'
