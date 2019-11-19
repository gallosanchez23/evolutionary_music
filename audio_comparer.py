"""
1. Decode mp3 to PCM.
2. Ensure that PCM data has specific sample rate, which you choose beforehand (e.g. 16KHz). You'll need to resample songs that have different sample rate. High sample rate is not required since you need a fuzzy comparison anyway, but too low sample rate will lose too much details.
3. Normalize PCM data (i.e. find maximum sample value and rescale all samples so that sample with largest amplitude uses entire dynamic range of data format, e.g. if sample format is signed 16 bit, then after normalization max. amplitude sample should have value 32767 or -32767).
4. Split audio data into frames of fixed number of samples (e.g.: 1000 samples per frame).
5. Convert each frame to spectrum domain (FFT).
6. Calculate correlation between sequences of frames representing two songs. If correllation is greater than a certain threshold, assume the songs are the same.
"""
import numpy as np

import acoustid
import chromaprint

# seconds to sample audio file for
sample_time = 500
# number of points to scan cross correlation over
span = 22
# step size (in points) of cross correlation
step = 1
# minimum number of points that must overlap in cross correlation
# exception is raised if this cannot be met
min_overlap = 5
# report match when cross correlation has a peak exceeding threshold
threshold = 0.5

# calculate fingerprint
def calculate_fingerprints(filename):
    # duration, fp_encoded = acoustid.fingerprint_file(filename)
    print(filename)
    duration, fp_encoded = acoustid.fingerprint(samplerate=filename[0], channels=filename[1], pcmiter=filename[2])

    fingerprint, version = chromaprint.decode_fingerprint(fp_encoded)
    # print(fingerprint)

    return fingerprint
  
# returns correlation between lists
def correlation(listx, listy):
    if len(listx) == 0 or len(listy) == 0:
        # Error checking in main program should prevent us from ever being
        # able to get here.
        raise Exception('Empty lists cannot be correlated.')
    if len(listx) > len(listy):
        listx = listx[:len(listy)]
    elif len(listx) < len(listy):
        listy = listy[:len(listx)]
    
    covariance = 0
    for i in range(len(listx)):
        covariance += 32 - bin(listx[i] ^ listy[i]).count("1")
    covariance = covariance / float(len(listx))
    
    return covariance/32

def correlate(source, target):
    global span
    fingerprint_source = calculate_fingerprints(source)
    fingerprint_target = calculate_fingerprints(target)
    
    span = len(fingerprint_source)
    corr = correlation(fingerprint_source, fingerprint_target)
    return corr
