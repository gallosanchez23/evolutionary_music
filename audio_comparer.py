import acoustid
import chromaprint
from pydub import AudioSegment
import numpy as np
from scipy import stats, signal

from scipy.io import wavfile as wav
from scipy.fftpack import rfft
from sklearn.metrics import mean_squared_error


class AudioComparer():

	def __init__(self, target_name):
		self.target_name = target_name
		self.target_fingerprint = self.get_fingerprint(target_name)

		rate, data = wav.read(target_name)
		self.target_fft = rfft(data)

	def get_fingerprint(self, file_name):
		duration, fp_encoded = acoustid.fingerprint_file(file_name)
		fingerprint, version = chromaprint.decode_fingerprint(fp_encoded)

		return fingerprint

	def compare(self, source_name: str, comparison='fingerprint'):
		if comparison == 'fingerprint':
			fingerprint = self.get_fingerprint(source_name)

			correlation = self.correlation(fingerprint)
			return correlation
		elif comparison == 'fft':
			return self.fft_compare(source_name)
		# return self.signal_to_noise(source_name)

	def correlation(self, source_fingerprint):
		source = source_fingerprint
		target = self.target_fingerprint

		if len(source) == 0 or len(target) == 0:
			return 0.0

		if len(source) > len(target):
			source = source[:len(target)]
		elif len(source) < len(target):
			target = target[:len(source)]

		covariance = 0
		for i in range(len(source)):
			covariance += 32 - bin(source[i] ^ target[i]).count('1')
		covariance = covariance / float(len(source))

		return covariance / 32

	def fft_compare(self, file_name):
		rate, data = wav.read(file_name)
		fft_out = rfft(data)
		return mean_squared_error(self.target_fft, fft_out)
		

	def get_ms_frames(self, segment, ms=350):
		ms_frames = []
		start = 0
		duration = segment.shape[0]
		while duration > 0:
			ms_frames.append(segment[start:start + 350])
			duration -= 350
		return np.array(ms_frames)

	def signal_to_noise(self, file_name):
		source = AudioSegment.from_wav(file_name)
		np_source = np.array(source.get_array_of_samples())

		target = AudioSegment.from_wav(self.target_name)
		np_target = np.array(target.get_array_of_samples())

		np_added = np_target + np_source
		ratio = self.signaltonoise(np_added)
		print(ratio)
		return ratio


	def signaltonoise(a, axis=0, ddof=0):
		a = np.asanyarray(a)
		m = a.mean(axis)
		sd = a.std(axis=axis, ddof=ddof)
		return np.where(sd == 0, 0, m/sd)
