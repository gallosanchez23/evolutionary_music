import acoustid
import chromaprint

class AudioComparer():

	def __init__(self, target_name):
		self.target_name = target_name
		self.target_fingerprint = self.get_fingerprint(target_name)

	def get_fingerprint(self, file_name):
		duration, fp_encoded = acoustid.fingerprint_file(file_name)
		fingerprint, version = chromaprint.decode_fingerprint(fp_encoded)

		return fingerprint

	def compare(self, source_name: str):
		fingerprint = self.get_fingerprint(source_name)

		correlation = self.correlation(fingerprint)
		return correlation

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
