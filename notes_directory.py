from pydub import AudioSegment

class NotesDirectory():

	def __init__(self):
		# List with the names of all available notes
		self.NOTES = [
			'A2', 'A3', 'A4', 'A5', 'A6', 'A7',
			'B2', 'B3', 'B4', 'B5', 'B6', 'B7',
			'C2', 'C3', 'C4', 'C5', 'C6', 'C7',
			'D2', 'D3', 'D4', 'D5', 'D6', 'D7',
			'E2', 'E3', 'E4', 'E5', 'E6', 'E7',
			'F2', 'F3', 'F4', 'F5', 'F6', 'F7',
			'G2', 'G3', 'G4', 'G5', 'G6', 'G7',
			'S'
		]

		# List with the frequencies of all available notes
		self.NOTE_FREQUENCIES = [
			110.0, 220.0, 440.0, 880.0, 1760.0, 3520.0,
			123.47, 246.94, 493.88, 987.77, 1975.53, 3951.07,
			65.41, 130.81, 261.63, 523.25, 1046.50, 2093.00,
			73.42, 146.83, 293.66, 587.33, 1174.66, 2349.32,
			82.41, 164.81, 329.63, 659.26, 1318.51, 2637.02,
			87.31, 174.61, 349.23, 698.46, 1396.91, 2793.83,
			98.0, 196.0, 392.0, 783.99, 1567.98, 3135.96,
			0.0
		]

		# List with audio of each note on NOTES
		self.AUDIO_NOTES = []

		for note in self.NOTES:
			self.AUDIO_NOTES.append(
				AudioSegment.from_wav(f'data/half_notes/{note}.wav')
			)

	def get_audio_note(self, index: int) -> AudioSegment:
		return self.AUDIO_NOTES[index]
