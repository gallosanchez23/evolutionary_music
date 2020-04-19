import os, glob, wave, csv

path = 'data/full_notes_88'
new_path = 'data/half_notes_88'

def process_notes():
    global path, new_path
    for filename in glob.glob(os.path.join(path, '*.wav')):
        audio = wave.open(filename, 'r')
        framerate = audio.getframerate()
        channels = audio.getnchannels()
        samp = audio.getsampwidth()

        chunk = audio.readframes(int(0.350 * framerate))

        new = wave.open(filename.replace("full_notes_88", "half_notes_88"), 'w')
        new.setnchannels(channels)
        new.setsampwidth(samp)
        new.setframerate(framerate)
        new.writeframes(chunk)
        new.close()
        audio.close()

def print_notes():
    global path, new_path
    appended = []
    for filename in glob.glob(os.path.join(path, '*.wav')):
        sections = filename.split('/')
        note = sections[2].split('.')[0]
        appended.append(f"'{note}'")
    appended.sort()
    print(','.join(appended))

def generate_frequency_dictionary():
    with open('note_frequencies.csv', 'r') as infile:
        reader = csv.reader(infile)
        freq_dict = {row[0]:float(row[1]) for row in reader}
        return freq_dict

test = generate_frequency_dictionary()
print(test)