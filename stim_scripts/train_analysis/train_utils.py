import mido 
import pandas as pd
import numpy as np
import ast

#IMPORTANT FUNCTIONS FOR RESULTS

#---------------------PREPARING MIDI OF EXAMPLE MELODIES-----------------------------

"""Load the MIDI file with the stuff recorded in ableton (aka the correct target notes)
target_midi: an imported midi file. Can use mido.MidiFile('file.mid')
returns a list of lists with 4 elements each. Each of the 4-item lists represents a melody

example:
testfile = mido.MidiFile('midi_target/easy_pt1.mid')
test = midi_target(testfile)
"""

def midi_target(midi_file, chunksize=4):
    target_midi = mido.MidiFile(midi_file)
    target_notes = []
    for message in target_midi.tracks[0]:
        if message.type == "note_on":
            target_notes.append(message.note)

    split_list = [target_notes[i:i + chunksize] for i in range(0, len(target_notes), chunksize)]
    return split_list

#getting all the split lists from the files
#importing the recorded midi files

"""cd = midi_target('../raw_training_files_wurli/cd.mid')
cde = midi_target('../raw_training_files_wurli/cde.mid')
cdef = midi_target('../raw_training_files_wurli/cdef.mid')
d_ef = midi_target('../raw_training_files_wurli/def.mid')
efg = midi_target('../raw_training_files_wurli/efg.mid')
ef = midi_target('../raw_training_files_wurli/ef.mid')
fg = midi_target('../raw_training_files_wurli/fg.mid')
cdefg = midi_target('../raw_training_files_wurli/cdefg.mid')"""
exampleset = midi_target('../raw_training_files_wurli/passive listening.mid')

#append the files in the correct presentation order to have the full set 

#-------------------------------PREPARING DATA FOR ANALYSIS-----------------------------
"""
categorizes the example melodies according to their type (i.e. which notes were in the melody)
"""
def categorize_list(lst):
    x = len(set(lst))
    if x == 1:
        return 1
    elif x == 2:
        return 2
    elif x == 3:
        return 3
    elif x == 4: 
        return 4
    else:
        return None

"""Calculate score
This calculates a score on the participant response based on the following criteria:
1. For each index of the list where the note at that index matches the correct note, I give it one point
2. For each note that is wrong, I give a partial point. The amount of points awarded depends on the difference between 
the note that is played and the correct note. For example, playing midi note 69 awards more points than note 72 if the
 correct note was 65

 correct notes: target MIDI vector
 played_notes: notes_vector
"""
def pad_vec(vec):
    while len(vec)<4:
        vec.append(0)
    return np.array(vec)

def calc_score(correct_notes, played_notes):
    correct_array = pad_vec(correct_notes)
    played_array = pad_vec(played_notes)

    exact_matches = np.sum(correct_array == played_array) #notes that were correct and in the correct position
    differences = np.abs(correct_array - played_array) #notes that were wrong: how far off are they?

    partial_scores = [1 - 0.1 * x if x != 0 else 0 for x in differences]

    total_score = exact_matches + np.sum(partial_scores)
    
    return total_score

""" 
Setting up a dataframe with participant data 
file: the csv file with the participant responses
exampleset: the list of MIDI melodies corresponding to the correct melodies

example:
result_file = 'cindy_test2.csv' <-- one file for each participant
fullset = cd+cde <-- define the melodies used in the psychopy test
results = resp_pd(result_file, fullset)
"""
def resp_pd(file, exampleset):
    print(file)
    #load user responses
    #make sure that the length of target column is same as length of results
    results = pd.read_csv(file)

    results['subject'] = file.split('.')[0][-2:]
    #participant responses are lists embedded in strings so we have to change it back to a list
    results['notes_vector'] = [ast.literal_eval(x) for x in results['notes_vector']] 

    #adding the target column with the MIDI of the example melodies
    results['target'] = exampleset

    #calculating whether each individual response is perfect
    results['correct'] = results.apply(lambda row: 1 if row['notes_vector'] == row['target'] else 0, axis=1)

    #calculate scores based on manually defined criteria
    results['score'] = results.apply(lambda row: calc_score(row['target'][0:4], row['notes_vector'][0:4]), axis = 1 )

    #add the block number
    rows_per_block = 82 #might be changed in the future
    results['block'] = np.repeat(np.arange(1, len(results) // rows_per_block + 1), rows_per_block)

    #add the block index (ie how difficult one part of the block is; cd vs cde vs cdefg and so on...)
    results['type'] = results['target'].apply(categorize_list)

    return results