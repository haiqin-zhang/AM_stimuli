"""
a better version of split.py that allows you to specify the file to split, the destination folder, and root of the file name.
to run: python snip.py [file to split] [destination folder] [root name] 

puts a leading number on the root name to control the order in which the melodies are played in the training program
make sure the recording volume in ableton is high enough, otherwise some notes are mistaken for silence

EXAMPLE: 
python snip.py def.wav ./wav_new/ def


"""

from pydub import AudioSegment
from pydub.silence import split_on_silence
import sys
import os

def split_wav(input_file, output_folder, file_name_root="snippet", silence_threshold=-40):
    sound = AudioSegment.from_wav(input_file)

    # Split on silence with a minimum silence duration of 1000 milliseconds
    snippets = split_on_silence(sound, silence_thresh=silence_threshold, min_silence_len=2000)

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Save each snippet to a separate file
    for i, snippet in enumerate(snippets):
       padded_index = str(i + 1).zfill(2)
       snippet.export(f"{output_folder}/{file_name_root}_{padded_index}.wav", format="wav")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_file> <output_folder> [file_name_root]")
    else:
        input_file = sys.argv[1]
        output_folder = sys.argv[2]
        file_name_root = sys.argv[3] if len(sys.argv) > 3 else "snippet"

        split_wav(input_file, output_folder, file_name_root)
