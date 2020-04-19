import polyphonic

from evolutionary_music import evo_music
from audio_comparer import AudioComparer
import pandas as pd

source_path = "data/songs"
dest_path = "data/generated_songs"
results_dest_path = "data/results"

from os import listdir
from os.path import isfile, join

onlyfiles = [f for f in listdir(source_path) if isfile(join(source_path, f))]
print(onlyfiles)
for f in onlyfiles:
    # if "jingle" not in f:
    #     continue
    comparer = AudioComparer(join(source_path, f))
    print(f)
    song_df = {
        "runs": [],
        "song": [],
        # "fitnesses": [],
        "mse": []
    }
    source = join(source_path, f)
    dest = join(dest_path, f)
    for i in range(30):
        print("Run", i)
        front = polyphonic.poly(source, dest)
        song_df["runs"].append(i)
        song_df["song"].append(f)
        # song_df["fitnesses"].append(front.objectives[0])
        song_df["mse"].append(comparer.compare(dest))
        for j in range(len(front)):
            if song_df.get(str(j)) is not None:
                song_df[str(j)].append(front[j])
            else:
                song_df[str(j)] = [front[j]]
    song_df = pd.DataFrame(song_df)
    song_df.to_csv(join(results_dest_path,f.split(".")[0] + "_poly.csv"))