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

		# List with audio of each note on NOTES
		self.AUDIO_NOTES = []

		for note in self.NOTES:
			self.AUDIO_NOTES.append(
				AudioSegment.from_wav(f'data/half_notes/{note}.wav')
			)

	def get_note(self, index: int) -> AudioSegment:
		return self.AUDIO[index]

	def get_audio_note(self, index: int) -> AudioSegment:
		return self.AUDIO_NOTES[index]
