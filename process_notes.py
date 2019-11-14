import os, glob, wave

path = 'data/full_notes'
new_path = 'data/half_notes'
for filename in glob.glob(os.path.join(path, '*.wav')):
    audio = wave.open(filename, 'r')
    framerate = audio.getframerate()
    channels = audio.getnchannels()
    samp = audio.getsampwidth()

    chunk = audio.readframes(int(0.350 * framerate))

    new = wave.open(filename.replace("full_notes", "half_notes"), 'w')
    new.setnchannels(channels)
    new.setsampwidth(samp)
    new.setframerate(framerate)
    new.writeframes(chunk)
    new.close()
    audio.close()