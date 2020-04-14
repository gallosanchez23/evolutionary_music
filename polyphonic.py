import os
import argparse
import numpy as np
import vamp

from librosa import load
from notes_directory import NotesDirectory
from pydub import AudioSegment
from scoreevent import Note

class PolyTrans(object):
    def __init__(self, step_size=441, hop_size=441):
        self._step_size = step_size
        self._hop_size = hop_size

    def transcribe(self, audio_path):
        if not os.path.exists(audio_path):
            raise ValueError('Invalid audio path')

        x, fs = load(audio_path, mono=True)

        notes = vamp.collect(x, fs, "qm-vamp-plugins:qm-transcription", output="transcription")['list']
        # access attributes of a note event by:
        # ts: f.timestamp
        # duration: f.duration
        # MIDI notes: f.values

        return notes

def generate_audio_file(notes, dest):
    notes_directory = NotesDirectory()

    combined = AudioSegment.empty()
    idxs = []
    for var in notes:
        idx = notes_directory.NOTES.index(var)
        combined += notes_directory.get_audio_note(idx)
        idxs.append(idx)
    combined.export(dest, format = 'wav')

    return idxs

def poly(source='data/songs/elise2.wav', dest='data/generated_songs/elise2_poly.wav'):
    t = PolyTrans()
    note_events = t.transcribe(source)

    song_events = []
    for n in note_events:
        midi_num = int(n['values'][0])+1
        pname, oct = Note.midi_to_pitch(midi_num)
        song_events.append(str(pname) + str(oct))
    idxs = generate_audio_file(song_events, dest)

    return idxs