import pandas as pd
import mido
import ast
import matplotlib.pyplot as plt
import numpy as np
import scipy
import glob
import os

from utils.train_utils import *

"""
Simple file to get per-trial scores from the training session. 

To run: cd train_analysis
python get_scores.py

By default skips the files that have already been processed. If you want to recalculate the scores for all files, set redo below to True
"""

redo = False

# PARAMETERS
# Define the number of cycles in the training
numcycles = 2
exampleset = midi_target('../raw_training_files_wurli/passive listening.mid')
fullset = exampleset * numcycles

root_dir = "/Users/cindyzhang/Documents/M2/Audiomotor_Piano/AM_stimuli/stim_scripts/train_analysis/raw_keystrokes"
output_dir = "/Users/cindyzhang/Documents/M2/Audiomotor_Piano/AM_stimuli/stim_scripts/train_analysis/scores"

files = glob.glob(os.path.join(root_dir, '**', '*.csv'), recursive=True)

for sub_file in files:
    sub_name = sub_file.split('.')[0][-2:]
    output_file = os.path.join(output_dir, f'scores_sub_{sub_name}.csv')
    
    # Check if the output file already exists
    if os.path.exists(output_file) and redo == False:
        print("Skipping ", sub_name, "- File already processed")
        continue
    
    print("Processing ", sub_name)
    
    subj_res = resp_pd(sub_file, fullset)
    subj_res.to_csv(output_file, index=False)
